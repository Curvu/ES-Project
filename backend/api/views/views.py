from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..utils import require_params, authenticated
from ..models import Service
from django.utils.dateparse import parse_datetime

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
        service_type=service_type,
        datetime=parse_datetime(datetime),
    )

    if booking == 0:
        return JsonResponse({"error": "Schedule already taken."}, status=400)
    elif booking == -1:
        return JsonResponse({"error": "User already has a booking for this service."}, status=400)
    elif booking == -2:
        return JsonResponse({"error": "Cannot book in the past."}, status=400)
    elif not booking:
        return JsonResponse({"error": "Failed to book service"}, status=500)

    return JsonResponse({"message": "Service booked successfully"}, status=200)

@api_view(["GET"])
@authenticated
def get_bookings(request, user, token):
    services = Service.objects.filter(user=user)
    return JsonResponse({"bookings": [s.to_dict() for s in services]}, status=200)
