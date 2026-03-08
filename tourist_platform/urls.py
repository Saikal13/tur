from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import register_page, login_page, home, api_page, logout_page

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.shortcuts import render
from django.db.models import Count
from tours.models import Country
from bookings.views import bookings_page


def countries_grid(request):
    countries = Country.objects.annotate(tours_count=Count("tours")).order_by("name")
    return render(request, "countries_grid.html", {"countries": countries})


schema_view = get_schema_view(
    openapi.Info(
        title="Tourist Platform API",
        default_version="v1",
        description="API для туров, бронирований и отзывов",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("register/", register_page, name="register_page"),
    path("login/", login_page, name="login_page"),
    path("logout/", logout_page, name="logout"),

    path("", home, name="home"),
    path("api-page/", api_page, name="api_page"),

    path("admin/", admin.site.urls),

    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    # API
    path("api/users/", include("users.urls")),
    path("api/tours/", include("tours.urls")),
    path("api/trips/", include("trips.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/bookings/", include("bookings.urls")),

    # HTML / UI
    # path("bookings/", bookings_page, name="bookings_page"),
    # path(
    #     "bookings/request/<int:tour_id>/",
    #     BookingRequestHTMLView.as_view(),
    #     name="booking_request_html",
    # ),

    path("trips/", include("trips.ui_urls")),
    path("tours/", include("tours.ui_urls")),
    path("flights/", include("flights.urls")),
    path("countries/", countries_grid, name="countries_grid"),

    path("api-auth/", include("rest_framework.urls")),
    path('admin-panel/', include('admin_panel.urls')),
    path('client/', include('client_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)