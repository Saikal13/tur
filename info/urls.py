from django.urls import path
from .views import country_detail, attraction_detail, event_detail

app_name = 'info'

urlpatterns = [
    path('countries/<int:country_id>/', country_detail, name='country_detail'),
    path('attractions/<int:attraction_id>/', attraction_detail, name='attraction_detail'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
]