from django.urls import path
from .views import trips_page

urlpatterns = [
    path("", trips_page, name="trips_page"),
]