from django.db import models
from django.contrib.auth.models import User
from tours.models import Tour


class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая"),
        ("in_progress", "В работе"),
        ("done", "Завершена"),
        ("canceled", "Отменена"),
    ]

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, default="")

    tour = models.ForeignKey(
        Tour,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="booking_requests",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    comment = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} • {self.phone} • {self.status}"