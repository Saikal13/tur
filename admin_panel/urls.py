from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('bookings/', views.bookings_list, name='bookings_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('users/', views.users_list, name='users_list'),
    path('tours/', views.tours_list, name='tours_list'),
    path('stats/', views.stats, name='stats'),
    path('client-responses/', views.client_responses_list, name='client_responses_list'),  # ✅ НОВОЕ
]