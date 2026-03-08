from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import Country, Tour, City, TourDay, TourHotel
from .serializers import CountrySerializer, TourSerializer
from .permissions import IsAdminOrReadOnly


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    template_name = "countries_grid.html"
    template_name_detail = "country_detail.html"

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]

    ordering_fields = ["name", "id", "tours_count"]
    ordering = ["-tours_count", "name"]

    def get_queryset(self):
        qs = Country.objects.all()

        visa_free = self.request.query_params.get("visa_free")
        if visa_free in ("1", "true", "True", "yes", "on"):
            qs = qs.filter(visa_free=True)

        vacation_type = self.request.query_params.get("vacation_type")
        if vacation_type and vacation_type != "any":
            qs = qs.filter(vacation_type=vacation_type)

        departure_city = self.request.query_params.get("departure_city")
        if departure_city:
            qs = qs.filter(tours__departure_city=departure_city).distinct()
            qs = qs.annotate(
                tours_count=Count("tours", filter=Q(tours__departure_city=departure_city))
            )
        else:
            qs = qs.annotate(tours_count=Count("tours"))

        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.accepted_renderer.format == "html":
            return Response({"countries": queryset}, template_name=self.template_name)

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        country = self.get_object()

        tours_count = Tour.objects.filter(country=country).count()
        tours = Tour.objects.filter(country=country).order_by("-created_at")[:12]

        if request.accepted_renderer.format == "html":
            return Response(
                {"country": country, "tours_count": tours_count, "tours": tours},
                template_name=self.template_name_detail,
            )

        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.select_related("country", "owner", "city").all().order_by("-created_at")
    serializer_class = TourSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country", "difficulty", "departure_city"]

    search_fields = ["title", "description"]
    ordering_fields = ["price", "start_date", "duration_days", "created_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CountryDetailHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    template_name = "country_detail.html"

    def get(self, request, pk):
        country = get_object_or_404(Country, pk=pk)
        tours_count = Tour.objects.filter(country=country).count()
        return Response(
            {
                "country": country,
                "tours_count": tours_count,
            },
            template_name=self.template_name,
        )


class CountryToursHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    template_name = "country_tours_search.html"

    def get(self, request, pk):
        country = get_object_or_404(Country, pk=pk)

        cities = country.cities.all()

        qs = Tour.objects.select_related("country", "owner", "city").filter(
            country=country,
            is_active=True
        )

        departure_city = request.GET.get("departure_city", "bishkek")
        if departure_city:
            qs = qs.filter(departure_city=departure_city)

        city_name = (request.GET.get("city", "") or "").strip()
        if city_name:
            qs = qs.filter(Q(city__name__icontains=city_name))

        ordering = request.GET.get("ordering", "-created_at")
        allowed = {
            "-created_at",
            "created_at",
            "price",
            "-price",
            "start_date",
            "-start_date",
        }

        if ordering in allowed:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-created_at")

        return Response(
            {
                "country": country,
                "cities": cities,
                "tours": qs,
                "tours_count": qs.count(),
                "filters": {
                    "departure_city": departure_city,
                    "city": city_name,
                    "ordering": ordering,
                },
            },
            template_name=self.template_name,
        )


class TourDetailHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    template_name = "tour_detail.html"

    def get(self, request, pk):
        tour = get_object_or_404(
            Tour.objects.select_related("country", "city", "owner"),
            pk=pk,
            is_active=True,
        )

        # details
        if not tour.details:
            city_name = tour.city.name if tour.city else tour.country.name
            tour.details = (
                f"Тур в {city_name} — отличный вариант для отдыха и знакомства с местной культурой.\n\n"
                f"Вылет из города: {tour.get_departure_city_display()}.\n"
                f"Продолжительность: {tour.duration_days} дней.\n"
                f"Дата вылета: {tour.start_date}.\n\n"
                f"Во время поездки вас ждут прогулки, отдых, знакомство с достопримечательностями "
                f"и комфортное размещение."
            )

        # hotel
        if not tour.hotel_name:
            city_name = tour.city.name if tour.city else tour.country.name
            tour.hotel_name = f"{city_name} Central Hotel"

        tour.save()

        # days
        if not TourDay.objects.filter(tour=tour).exists():
            for i in range(1, tour.duration_days + 1):
                if i == 1:
                    title = "Прилёт и заселение"
                    description = "Вылет, прибытие, трансфер в отель, заселение и свободное время."
                elif i == tour.duration_days:
                    title = "Возвращение"
                    description = "Выселение из отеля, трансфер в аэропорт и обратный вылет."
                else:
                    title = f"День {i}"
                    description = "Экскурсии, прогулки, отдых и свободное время по программе тура."

                TourDay.objects.create(
                    tour=tour,
                    day_number=i,
                    title=title,
                    description=description,
                )

        # hotels
        if not TourHotel.objects.filter(tour=tour).exists():
            city_name = tour.city.name if tour.city else tour.country.name
            TourHotel.objects.create(
                tour=tour,
                name=f"{city_name} Central Hotel",
                description="Комфортный стандартный отель в удобной локации.",
                price_extra=0,
            )
            TourHotel.objects.create(
                tour=tour,
                name=f"{city_name} Premium Hotel",
                description="Улучшенный вариант с более высоким уровнем сервиса.",
                price_extra=120,
            )
            TourHotel.objects.create(
                tour=tour,
                name=f"{city_name} Family Hotel",
                description="Спокойный и удобный вариант для отдыха.",
                price_extra=80,
            )

        days = TourDay.objects.filter(tour=tour).order_by("day_number")
        hotels = TourHotel.objects.filter(tour=tour).order_by("name")

        return Response(
            {
                "tour": tour,
                "days": days,
                "hotels": hotels,
            },
            template_name=self.template_name,
        )