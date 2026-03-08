from django.contrib import admin
from .models import TourNotification


@admin.register(TourNotification)
class TourNotificationAdmin(admin.ModelAdmin):
    list_display = ('booking', 'country', 'departure_date', 'departure_time', 'is_sent', 'created_at')
    list_filter = ('is_sent', 'is_read', 'created_at')
    search_fields = ('booking__name', 'country', 'flight_number')
    readonly_fields = ('created_at', 'sent_at')

    fieldsets = (
        ('Заявка', {
            'fields': ('booking',)
        }),
        ('Детали вылета', {
            'fields': ('country', 'departure_date', 'departure_time', 'departure_airport', 'arrival_airport',
                       'flight_number')
        }),
        ('Статус', {
            'fields': ('is_sent', 'is_read', 'created_at', 'sent_at')
        }),
    )