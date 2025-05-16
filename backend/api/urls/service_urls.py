from django.urls import path
from api.views.service_views import (
    ServiceListView,
    ServiceDetailView,
    BookServiceView,
    UserBookingsView,
    PayServiceView,
    AdminBookingsView,
    AdminBookingView
)

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list'),
    path('<int:service_type>/', ServiceDetailView.as_view(), name='service-detail'),
    path('bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('book/', BookServiceView.as_view(), name='book-service'),
    path('pay/<uuid:service_id>/', PayServiceView.as_view(), name='pay-service'),

    path('admin-bookings/', AdminBookingsView.as_view(), name='admin-bookings'),
    path('admin-booking/', AdminBookingView.as_view(), name='admin-booking'),
]
