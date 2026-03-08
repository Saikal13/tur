from rest_framework import serializers
from .models import Trip, Expense


class TripSerializer(serializers.ModelSerializer):
    total_expenses = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ("id", "title", "start_date", "end_date", "budget", "total_expenses", "created_at")
        read_only_fields = ("id", "created_at", "total_expenses")

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Название поездки минимум 3 символа.")
        return value

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        budget = attrs.get("budget")

        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "Дата окончания не может быть раньше даты начала."})
        if budget is not None and budget < 0:
            raise serializers.ValidationError({"budget": "Бюджет не может быть отрицательным."})
        return attrs

    def get_total_expenses(self, obj):
        return sum((e.amount for e in obj.expenses.all()), start=0)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("id", "trip", "title", "amount", "date")
        read_only_fields = ("id",)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть больше 0.")
        return value