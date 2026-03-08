from django.db import models
from bookings.models import BookingRequest


class TourNotification(models.Model):
    """
    Уведомления клиентам о подтверждении тура и деталях вылета
    """
    booking = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, related_name='tour_notifications')

    # Детали вылета
    country = models.CharField(max_length=255)  # Страна назначения
    departure_date = models.DateField()  # Дата вылета
    departure_time = models.TimeField()  # Время вылета
    departure_airport = models.CharField(max_length=255, blank=True)  # Аэропорт вылета
    arrival_airport = models.CharField(max_length=255, blank=True)  # Аэропорт прилета
    flight_number = models.CharField(max_length=50, blank=True)  # Номер рейса

    # Статус
    is_sent = models.BooleanField(default=False)  # Отправлено ли уведомление
    is_read = models.BooleanField(default=False)  # Прочитано ли клиентом

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Уведомление для {self.booking.name} - {self.country}"