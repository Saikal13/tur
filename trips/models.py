from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from tours.models import Tour, Country
from django.conf import settings


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_trips",  # уникальное имя для связи
        null=True,  # разрешаем пустое поле для старых записей
        blank=True,
        verbose_name="Владелец"
    )
    title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    tour = models.ForeignKey(
        Tour,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trips"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trips"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # можно добавить безопасно

    @property
    def total_expenses(self):
        return self.expenses.aggregate(total=Sum("amount"))["total"] or 0

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Expense(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.title}: {self.amount}"