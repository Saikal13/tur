from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CountryViewSet,
    TourViewSet,
    CountryDetailHTMLView,
    CountryToursHTMLView
)

router = DefaultRouter()
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"tours", TourViewSet, basename="tours")

urlpatterns = [

    # ===== API (оставляем) =====
    path("", include(router.urls)),

    path("country/<int:pk>/", CountryDetailHTMLView.as_view(), name="country_detail_html"),
    path("country/<int:pk>/tours/", CountryToursHTMLView.as_view(), name="country_tours_html"),


    # ===== UI маршруты (добавлено) =====

    # /countries/
    path("", include([
        path("", CountryViewSet.as_view({'get': 'list'}), name="countries_page"),
    ])),

    # /countries/<id>/
    path("<int:pk>/", CountryDetailHTMLView.as_view(), name="country_page"),

    # /tours/country/<id>/tours/
    path("tours/country/<int:pk>/tours/", CountryToursHTMLView.as_view(), name="country_tours_page"),
]