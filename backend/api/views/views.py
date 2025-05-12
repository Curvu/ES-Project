from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..utils import require_params, authenticated, get_stepfunctions_client
from ..models import Service
from ..dynamodb import get_status
from django.utils.dateparse import parse_datetime
import json

@api_view(["GET"])
@authenticated
def get_all_services(request, user, token):
    return JsonResponse({ "services": Service.get_all_service_prices(user) }, status=200)

@api_view(["GET"])
@authenticated
def get_service(request, user, token, service_id):
    try:
        service_type = Service.Types(service_id)
    except ValueError:
        return JsonResponse({"error": "Invalid service type ID"}, status=400)

    return JsonResponse({
        "id": service_id,
        "name": service_type.label,
        "price": Service.PRICES.get(service_id),
        "can_book": Service.user_can_book(user, service_type),
    })

@api_view(["POST"])
@authenticated
@require_params("service_id", "datetime")
def book_service(request, user, token):
    service_id = request.data["service_id"]
    datetime = request.data["datetime"]

    try:
        service_type = Service.Types(int(service_id))
    except ValueError:
        return JsonResponse({"error": "Invalid service type ID"}, status=400)

    booking = Service.book_service(
        user=user,
        type=service_type,
        datetime=parse_datetime(datetime),
    )

    if booking == 0:
        return JsonResponse({"error": "Error booking."}, status=400)

    try:
        stepfunctions = get_stepfunctions_client()

        stepfunctions.start_execution(
            stateMachineArn='arn:aws:states:us-east-1:000000000000:stateMachine:BookingWorkflow',
            input=json.dumps({
                "service_id": str(booking.id),
                "schedule_time": datetime,
            })
        )

        return JsonResponse({"message": "Service booked successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": "Failed to start step function", "details": str(e)}, status=500)


@api_view(["GET"])
@authenticated
def get_bookings(request, user, token):
    services = Service.objects.filter(user=user)
    return JsonResponse({"bookings": [s.to_dict() for s in services]}, status=200)
