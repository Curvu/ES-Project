from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..utils import require_params, authenticated, get_stepfunctions_client
from ..models import Service
from ..dynamodb import update_status, get_status
from django.utils.dateparse import parse_datetime

@api_view(["GET"])
@authenticated
def admin_get_bookings(request, user, token):
    if not user.is_admin:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    services = Service.objects.all()
    return JsonResponse({"bookings": [s.to_dict() for s in services]}, status=200)

@api_view(["PUT"])
@authenticated
@require_params("booking_id", "state")
def admin_set_booking(request, user, token):
    if not user.is_admin:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    service_id = request.data.get("booking_id")
    state = request.data.get("state")

    print(f"Setting booking {service_id} to state {state}")

    service = Service.objects.filter(id=service_id).first()
    if not service:
        return JsonResponse({"error": "Service not found"}, status=404)

    status = get_status(service_id)
    if not status:
        return JsonResponse({"error": "Service status not found"}, status=404)

    paid = status.get("paid", False)

    if state == 4 and not paid:
        return JsonResponse({"error": "Cannot set state to 'completed' without payment"}, status=400)

    update_status(service_id, "sstate", state)

    return JsonResponse({"message": "Booking updated successfully", "state": state}, status=200)