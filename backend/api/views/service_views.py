from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Service
from api.utils import get_stepfunctions_client, get_auth_header_parameter
from api.decorators import authenticated, validate_request
from api.dynamodb import update_status, get_status
from api.serializers import (
    ServiceSerializer,
    ServiceTypeSerializer,
    BookServiceRequestSerializer,
    SetBookingStateRequestSerializer
)
from django.utils.dateparse import parse_datetime
import json
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema, OpenApiResponse


@method_decorator(authenticated, name='dispatch')
class ServiceListView(APIView):
    @extend_schema(
        summary="List all available services",
        description="Returns a list of all available services with their prices and booking capabilities.",
        parameters=get_auth_header_parameter(),
        responses={
            200: ServiceTypeSerializer(many=True),
            400: OpenApiResponse(description="Bad request, e.g. invalid parameters"),
            500: OpenApiResponse(description="Internal server error")
        }
    )
    def get(self, request, user, token):
        return Response({"services": ServiceTypeSerializer(list(Service.Types), many=True, context={'user': user}).data}, status=status.HTTP_200_OK)


@method_decorator(authenticated, name='dispatch')
class ServiceDetailView(APIView):
    @extend_schema(
        summary="Get service details",
        description="Returns details of a specific service type including its price and booking capability.",
        parameters=get_auth_header_parameter(),
        responses={
            200: ServiceSerializer,
            400: OpenApiResponse(description="Bad request, e.g. invalid service type ID"),
            404: OpenApiResponse(description="Service not found"),
            500: OpenApiResponse(description="Internal server error")
        }
    )
    def get(self, request, user, token, service_type):
        try:
            service_type = Service.Types(service_type)
        except ValueError:
            return Response({"error": "Invalid service type ID"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ServiceTypeSerializer(service_type, context={'user': user}).data, status=status.HTTP_200_OK)


@method_decorator(authenticated, name='dispatch')
class UserBookingsView(APIView):
    @extend_schema(
        summary="Get user bookings",
        description="Returns a list of all bookings made by the user.",
        parameters=get_auth_header_parameter(),
        responses={
            200: ServiceSerializer(many=True),
            403: OpenApiResponse(description="Forbidden, e.g. user not authenticated"),
            500: OpenApiResponse(description="Internal server error")
        }
    )
    def get(self, request, user, token):
        services = Service.objects.filter(user=user)
        return Response({"bookings": ServiceSerializer(services, context={'user': user}, many=True).data}, status=status.HTTP_200_OK)


@method_decorator(authenticated, name='dispatch')
class BookServiceView(APIView):
    @extend_schema(
        summary="Book a service",
        description="Allows a user to book a service by specifying the service type and datetime.",
        parameters=get_auth_header_parameter(),
        request=BookServiceRequestSerializer,
        responses={
            200: OpenApiResponse(description="Booking successful"),
            400: OpenApiResponse(description="Bad request, e.g. invalid service type ID or booking failed"),
            500: OpenApiResponse(description="Internal server error during Step Functions execution")
        }
    )
    @validate_request(BookServiceRequestSerializer)
    def post(self, request, user, token, payload):
        datetime = payload.get("datetime")

        try:
            service_type = Service.Types(int(payload.get("service_id")))
        except ValueError:
            return Response({"error": "Invalid service type ID"}, status=status.HTTP_400_BAD_REQUEST)

        booking = Service.book_service(
            user=user,
            type=service_type,
            datetime=parse_datetime(datetime),
        )

        if booking == 0:
            return Response({"error": "Booking failed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stepfunctions = get_stepfunctions_client()
            stepfunctions.start_execution(
                stateMachineArn='arn:aws:states:us-east-1:000000000000:stateMachine:BookingWorkflow',
                input=json.dumps({
                    "service_id": str(booking.id),
                    "schedule_time": datetime,
                })
            )
            return Response({"message": "Booked successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Step function failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(authenticated, name='dispatch')
class PayServiceView(APIView):
    @extend_schema(
        summary="Pay for a service",
        description="Allows a user to pay for a booked service.",
        parameters=get_auth_header_parameter(),
        responses={
            200: OpenApiResponse(description="Payment successful"),
            400: OpenApiResponse(description="Payment failed, e.g. service not found or already paid"),
            403: OpenApiResponse(description="Forbidden, e.g. user not authenticated"),
            500: OpenApiResponse(description="Internal server error during payment processing")
        }
    )
    def post(self, request, user, token, service_id):
        success = Service.pay_service(service_id, user)
        if not success:
            return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)


@method_decorator(authenticated, name='dispatch')
class AdminBookingsView(APIView):
    @extend_schema(
        summary="Get all bookings for admin",
        description="Returns a list of all bookings for admin users.",
        parameters=get_auth_header_parameter(),
        responses={
            200: ServiceSerializer(many=True),
            403: OpenApiResponse(description="Forbidden, e.g. user not authenticated or not an admin"),
            500: OpenApiResponse(description="Internal server error")
        }
    )
    def get(self, request, user, token):
        if not user.is_admin:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        services = Service.objects.all()
        return Response({"bookings": ServiceSerializer(services, context={'user': user}, many=True).data}, status=status.HTTP_200_OK)


@method_decorator(authenticated, name='dispatch')
class AdminBookingView(APIView):
    @extend_schema(
        summary="Update booking state for admin",
        description="Allows an admin to update the state of a booking.",
        parameters=get_auth_header_parameter(),
        request=SetBookingStateRequestSerializer,
        responses={
            200: OpenApiResponse(description="Booking updated successfully"),
            400: OpenApiResponse(description="Bad request, e.g. invalid state or service not found"),
            403: OpenApiResponse(description="Forbidden, e.g. user not authenticated or not an admin"),
            404: OpenApiResponse(description="Service status not found"),
            500: OpenApiResponse(description="Internal server error during status update")
        }
    )
    @validate_request(SetBookingStateRequestSerializer)
    def put(self, request, user, token, payload):
        if not user.is_admin:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        service_id = payload.get("service_id")
        state = payload.get("state")

        service = Service.objects.filter(id=service_id).first()
        if not service:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        ss = get_status(service_id)
        if not ss:
            return Response({"error": "Service status not found"}, status=status.HTTP_404_NOT_FOUND)

        paid = ss.get("paid", False)

        if state == 4 and not paid:
            return Response({"error": "Cannot set state to 'completed' without payment"}, status=status.HTTP_400_BAD_REQUEST)

        update_status(service_id, "sstate", state)

        return Response({"message": "Booking updated successfully"}, status=status.HTTP_200_OK)