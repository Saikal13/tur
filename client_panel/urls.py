from django.urls import path
from . import views

urlpatterns = [
    # Заявки
    path('booking/<int:booking_id>/', views.booking_status, name='client_booking_status'),
    path('booking/<int:booking_id>/<str:email>/', views.booking_status_public, name='client_booking_status_public'),

    # Сообщения (приватные)
    path('messages/', views.client_messages, name='client_messages'),
    path('messages/count/', views.client_messages_count, name='client_messages_count'),
    path('messages/mark-read/', views.mark_messages_as_read, name='mark_messages_as_read'),

    # Сообщения (публичные)
    path('messages/<str:email>/', views.client_messages_public, name='client_messages_public'),
]