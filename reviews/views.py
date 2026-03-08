from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from tours.models import Tour


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "tour").all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filterset_fields = ["tour", "rating"]
    ordering_fields = ["created_at", "rating"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@login_required(login_url="/login/")
def reviews_page(request):
    reviews = Review.objects.select_related("user", "tour").all().order_by("-created_at")
    tours = Tour.objects.all().order_by("title")

    context = {
        "reviews": reviews,
        "tours": tours,
    }
    return render(request, "reviews_page.html", context)