from django.db import models
from django.contrib.auth.models import User
from bookings.models import BookingRequest


class ClientResponse(models.Model):
    """
    Ответы клиентов на комментарии администратора
    """
    booking = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, related_name='client_responses')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ответ от {self.booking.name} к заявке #{self.booking.id}"