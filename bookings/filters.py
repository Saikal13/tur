from django.db import models
from django.db.models import Q
from django.utils import timezone
from rest_framework.filters import BaseFilterBackend


class BookingQueryFilterBackend(BaseFilterBackend):
    TRUE_VALUES = {"1", "true", "yes", "on"}

    def filter_queryset(self, request, queryset, view):
        trip_id = request.query_params.get("trip")
        booking_type = request.query_params.get("type")
        status_value = request.query_params.get("status")
        upcoming = request.query_params.get("upcoming")
        unpaid = request.query_params.get("unpaid")
        search = request.query_params.get("search")

        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)

        if booking_type:
            queryset = queryset.filter(type=booking_type)

        if status_value:
            queryset = queryset.filter(status=status_value)

        if upcoming and upcoming.lower() in self.TRUE_VALUES:
            queryset = queryset.filter(
                start_date__isnull=False,
                start_date__gte=timezone.now(),
            )

        if unpaid and unpaid.lower() in self.TRUE_VALUES:
            queryset = queryset.filter(price__gt=0).exclude(
                paid_amount__gte=models.F("price")
            )

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(provider__icontains=search)
                | Q(city__icontains=search)
                | Q(country__icontains=search)
                | Q(address__icontains=search)
                | Q(booking_reference__icontains=search)
                | Q(notes__icontains=search)
            )

        return queryset