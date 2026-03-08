from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', views.my_notifications, name='my_notifications'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
]