from django.db import models
from django.contrib.auth.models import User
from bookings.models import BookingRequest


class ClientNotification(models.Model):
    """
    Уведомления для клиента о статусе заявки
    """
    booking = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, related_name='client_notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Уведомление для {self.booking.name} - {self.title}"