from django.core.management.base import BaseCommand
from tours.models import Country, City


SEED = {
    "Австрия": ["Вена", "Зальцбург", "Инсбрук", "Грац"],
    "Турция": ["Анталья", "Стамбул", "Аланья", "Бодрум"],
    "ОАЭ": ["Дубай", "Абу-Даби", "Шарджа", "Рас-эль-Хайма"],
    "Таиланд": ["Бангкок", "Пхукет", "Паттайя", "Краби"],
    "Египет": ["Хургада", "Шарм-эль-Шейх", "Каир", "Луксор"],
    "Италия": ["Рим", "Милан", "Венеция", "Флоренция"],
    "Франция": ["Париж", "Ницца", "Канны", "Лион"],
    "Испания": ["Барселона", "Мадрид", "Валенсия", "Малага"],
    "Греция": ["Афины", "Салоники", "Крит", "Родос"],
    "Грузия": ["Тбилиси", "Батуми", "Кутаиси", "Боржоми"],
    "Казахстан": ["Алматы", "Астана", "Шымкент", "Актау"],
}


COUNTRY_DEFAULTS = {
    # можно менять как хочешь
    "visa_free": True,
    "vacation_type": "any",
    "description": "Популярное направление для отдыха. Выберите город и посмотрите доступные туры.",
    "about": "Красивая страна с интересной культурой, кухней и достопримечательностями. Здесь можно найти отдых на любой вкус.",
    "short_info": "Виза/перелёт/валюта: уточняйте при бронировании. Лучшее время для поездки зависит от сезона.",
    "image": "",
}


class Command(BaseCommand):
    help = "Создаёт страны и города (seed) автоматически"

    def handle(self, *args, **options):
        created_countries = 0
        created_cities = 0

        for country_name, cities in SEED.items():
            country, c_created = Country.objects.get_or_create(
                name=country_name,
                defaults=COUNTRY_DEFAULTS,
            )
            if c_created:
                created_countries += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Создана страна: {country.name}"))
            else:
                self.stdout.write(f"ℹ️ Страна уже есть: {country.name}")

            for city_name in cities:
                city, city_created = City.objects.get_or_create(
                    country=country,
                    name=city_name,
                )
                if city_created:
                    created_cities += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nГотово! Стран создано: {created_countries}, городов создано: {created_cities}"
        ))