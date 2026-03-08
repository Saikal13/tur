from django.contrib import admin
from .models import News, CountryFact, Attraction, Event


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'category', 'created_at', 'is_active')
    list_filter = ('country', 'category', 'created_at', 'is_active')
    search_fields = ('title', 'content', 'country__name')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('country', 'title', 'content', 'category')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Статус', {
            'fields': ('is_active', 'created_at')
        }),
    )


@admin.register(CountryFact)
class CountryFactAdmin(admin.ModelAdmin):
    list_display = ('country', 'fact', 'fact_type', 'created_at')
    list_filter = ('country', 'fact_type', 'created_at')
    search_fields = ('fact', 'country__name')
    readonly_fields = ('created_at',)


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'attraction_type', 'rating', 'created_at')
    list_filter = ('country', 'attraction_type', 'rating', 'created_at')
    search_fields = ('name', 'description', 'country__name')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('country', 'name', 'description', 'attraction_type')
        }),
        ('Координаты', {
            'fields': ('latitude', 'longitude')
        }),
        ('Рейтинг и медиа', {
            'fields': ('rating', 'image')
        }),
        ('Дата создания', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'event_type', 'start_date', 'end_date', 'rating')
    list_filter = ('country', 'event_type', 'start_date')
    search_fields = ('title', 'description', 'country__name')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('country', 'title', 'description', 'event_type')
        }),
        ('Даты', {
            'fields': ('start_date', 'end_date')
        }),
        ('Рейтинг и медиа', {
            'fields': ('rating', 'image')
        }),
        ('Дата создания', {
            'fields': ('created_at',)
        }),
    )