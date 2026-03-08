from rest_framework import serializers
from .models import BookingRequest


class BookingRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заявок на бронирование
    """
    tour_title = serializers.CharField(source="tour.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = BookingRequest
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "tour",
            "tour_title",
            "status",
            "status_display",
            "comment",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "tour_title",
            "status_display",
            "created_at",
        ]