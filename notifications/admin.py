from django.contrib import admin
from .models import TourNotification


@admin.register(TourNotification)
class TourNotificationAdmin(admin.ModelAdmin):
    list_display = ('booking', 'country', 'departure_date', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'country')
    search_fields = ('booking__name', 'booking__email', 'country')
    readonly_fields = ('created_at', 'sent_at')

    fieldsets = (
        ('Booking Info', {
            'fields': ('booking',)
        }),
        ('Flight Details', {
            'fields': ('country', 'departure_date', 'departure_time', 'departure_airport', 'arrival_airport',
                       'flight_number')
        }),
        ('Status', {
            'fields': ('is_sent', 'is_read', 'created_at', 'sent_at')
        }),
    )