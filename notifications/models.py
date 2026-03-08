from django.db import models
from bookings.models import BookingRequest


class TourNotification(models.Model):
    """
    Уведомления о подтвержденных турах
    Каждый пользователь видит ТОЛЬКО свои уведомления
    """
    booking = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, related_name='tour_notifications')

    # Детали вылета
    country = models.CharField(max_length=255)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    departure_airport = models.CharField(max_length=255, blank=True)
    arrival_airport = models.CharField(max_length=255, blank=True)
    flight_number = models.CharField(max_length=50, blank=True)

    # Статус
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking.name} - {self.country}"