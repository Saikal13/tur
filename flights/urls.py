from django.urls import path
from . import views

urlpatterns = [
    path("", views.flights, name="flights"),
    path("go/", views.flights_redirect, name="flights_redirect"),
    path("ticket/", views.ticket_demo, name="ticket_demo"),
]