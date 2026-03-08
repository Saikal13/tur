from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingRequestViewSet, BookingRequestHTMLView, bookings_page

router = DefaultRouter()
router.register(r"requests", BookingRequestViewSet, basename="booking-request")

urlpatterns = [
    # API endpoints
    path("", include(router.urls)),

    # HTML страницы
    path("bookings-ui/", bookings_page, name="bookings_ui"),
    path("request/<int:tour_id>/", BookingRequestHTMLView.as_view(), name="booking_request_html"),
]