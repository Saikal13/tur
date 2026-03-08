from django.urls import path
from . import views

urlpatterns = [
    # Главная панель
    path('', views.dashboard, name='admin_dashboard'),

    # Заявки
    path('bookings/', views.bookings_list, name='bookings_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),

    # Пользователи
    path('users/', views.users_list, name='users_list'),

    # Туры
    path('tours/', views.tours_list, name='tours_list'),

    # Статистика
    path('stats/', views.stats, name='admin_stats'),
]