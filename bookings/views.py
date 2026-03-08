from django.db import models
from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .filters import BookingQueryFilterBackend
from .models import BookingRequest
from .permissions import IsOwnerThroughTrip
from .serializers import BookingRequestSerializer
from tours.models import Tour


class BookingRequestViewSet(viewsets.ModelViewSet):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [BookingQueryFilterBackend]

    def get_queryset(self):
        return BookingRequest.objects.all().order_by("-created_at")

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        data = queryset.aggregate(
            total=Count("id"),
            new=Count("id", filter=models.Q(status="new")),
            in_progress=Count("id", filter=models.Q(status="in_progress")),
            done=Count("id", filter=models.Q(status="done")),
            cancelled=Count("id", filter=models.Q(status="canceled")),
        )

        return Response(data)


class BookingRequestHTMLView(LoginRequiredMixin, CreateView):
    """
    HTML форма для создания заявки на бронирование тура
    """
    model = BookingRequest
    fields = ["name", "phone", "email", "comment"]
    template_name = "booking_request.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour_id = self.kwargs.get("tour_id")
        context["tour"] = get_object_or_404(Tour, id=tour_id)
        return context

    def form_valid(self, form):
        tour_id = self.kwargs.get("tour_id")
        form.instance.tour_id = tour_id
        messages.success(self.request, "Заявка отправлена! Мы скоро вам перезвоним.")
        return super().form_valid(form)


def bookings_page(request):
    """
    Страница со списком бронирований
    """
    return render(request, "bookings_list.html")