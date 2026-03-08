from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch, Q
from tours.models import Country
from .models import News, CountryFact, Attraction, Event


def country_detail(request, country_id):
    """Страница страны со всей информацией"""

    # Получаем страну или 404
    country = get_object_or_404(Country, id=country_id)

    # Оптимизируем запросы к БД
    news = News.objects.filter(
        country=country,
        is_active=True
    ).order_by('-created_at')[:6]

    facts = CountryFact.objects.filter(
        country=country
    ).order_by('-created_at')[:6]

    attractions = Attraction.objects.filter(
        country=country
    ).order_by('-rating')[:6]

    events = Event.objects.filter(
        country=country
    ).order_by('-start_date')[:6]

    # Подсчитываем общее количество (для ссылки "Показать всё")
    news_count = News.objects.filter(country=country, is_active=True).count()
    facts_count = CountryFact.objects.filter(country=country).count()
    attractions_count = Attraction.objects.filter(country=country).count()
    events_count = Event.objects.filter(country=country).count()

    # Передаем в шаблон
    context = {
        'country': country,
        'news': news,
        'facts': facts,
        'attractions': attractions,
        'events': events,
        'news_count': news_count,
        'facts_count': facts_count,
        'attractions_count': attractions_count,
        'events_count': events_count,
    }

    return render(request, 'info_country_main_beauty.html', context)


def attraction_detail(request, attraction_id):
    """Детальная страница достопримечательности"""

    attraction = get_object_or_404(
        Attraction.objects.select_related('country'),
        id=attraction_id
    )

    # Получаем похожие достопримечательности
    similar_attractions = Attraction.objects.filter(
        country=attraction.country,
        attraction_type=attraction.attraction_type
    ).exclude(id=attraction_id)[:4]

    context = {
        'attraction': attraction,
        'country': attraction.country,
        'similar_attractions': similar_attractions,
    }

    return render(request, 'info_attraction_detail.html', context)


def event_detail(request, event_id):
    """Детальная страница события"""

    event = get_object_or_404(
        Event.objects.select_related('country'),
        id=event_id
    )

    # Получаем другие события в этой стране
    other_events = Event.objects.filter(
        country=event.country
    ).exclude(id=event_id).order_by('-start_date')[:3]

    context = {
        'event': event,
        'country': event.country,
        'other_events': other_events,
    }

    return render(request, 'info_event_detail.html', context)