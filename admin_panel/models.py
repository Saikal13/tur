from django.db import models
from django.contrib.auth.models import User
from bookings.models import BookingRequest


class AdminLog(models.Model):
    """
    Логирование действий администратора
    """
    ACTION_CHOICES = [
        ('status_changed', 'Статус изменён'),
        ('comment_added', 'Комментарий добавлен'),
        ('booking_viewed', 'Заявка просмотрена'),
    ]

    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_logs')
    booking = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, related_name='admin_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    old_value = models.CharField(max_length=255, blank=True, default="")
    new_value = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.admin.username} - {self.get_action_display()} - {self.booking.name}"


class AdminComment(models.Model):
    """
    Комментарии администратора к заявкам
    """
    booking = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, related_name='admin_comments')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.admin.username} к заявке {self.booking.name}"