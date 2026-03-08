from django.core.management.base import BaseCommand
from tours.models import Tour, TourDay, TourHotel


class Command(BaseCommand):
    help = "Заполнить туры деталями, днями и отелями"

    def handle(self, *args, **options):
        tours = Tour.objects.all()

        if not tours.exists():
            self.stdout.write(self.style.WARNING("Туры не найдены!"))
            return

        for tour in tours:
            city_name = tour.city.name if tour.city else tour.country.name
            country_name = tour.country.name
            departure_name = tour.get_departure_city_display()

            # Подробное описание
            if not tour.details or tour.details.startswith("ТЕСТ:") or "Тест" in tour.details:
                tour.details = f"""
Тур в {city_name}, {country_name} — это комфортное путешествие с вылетом из {departure_name}, удобным размещением и насыщенной программой отдыха.

В стоимость тура входит:
- авиаперелёт
- проживание
- трансфер
- базовая экскурсионная программа
- сопровождение

Этот тур подойдёт для тех, кто хочет совместить отдых, прогулки по городу, знакомство с культурой и комфортное размещение.
""".strip()

            # Отель по умолчанию
            if not tour.hotel_name or tour.hotel_name.startswith("ТЕСТ:"):
                tour.hotel_name = f"{city_name} Central Hotel 4*"

            tour.save()

            # Полностью очищаем старые тестовые/авто данные и создаём заново
            TourDay.objects.filter(tour=tour).delete()
            TourHotel.objects.filter(tour=tour).delete()

            # Программа по дням
            for i in range(1, tour.duration_days + 1):
                if i == 1:
                    title = "Прилёт и заселение"
                    description = (
                        f"Вылет из {departure_name}, прибытие в {city_name}, "
                        f"встреча в аэропорту, трансфер в отель, заселение и свободное время."
                    )
                elif i == 2:
                    title = f"Обзор {city_name}"
                    description = (
                        f"После завтрака обзорная прогулка по {city_name}, "
                        f"знакомство с основными достопримечательностями и свободное время."
                    )
                elif i == 3:
                    title = "Экскурсионный день"
                    description = (
                        "После завтрака экскурсии, прогулки по красивым местам, "
                        "свободное время для отдыха, фото и покупок."
                    )
                elif i == tour.duration_days:
                    title = "Возвращение домой"
                    description = (
                        "Завтрак, выселение из отеля, трансфер в аэропорт и обратный вылет."
                    )
                else:
                    title = f"День {i}"
                    description = (
                        "Свободное время, отдых, прогулки, шопинг или дополнительные экскурсии по желанию."
                    )

                TourDay.objects.create(
                    tour=tour,
                    day_number=i,
                    title=title,
                    description=description,
                )

            # 3 варианта отелей
            TourHotel.objects.create(
                tour=tour,
                name=f"{city_name} Central Hotel 4*",
                description="Комфортный отель в хорошем районе города.",
                price_extra=0,
            )
            TourHotel.objects.create(
                tour=tour,
                name=f"{city_name} Premium Hotel 4*+",
                description="Улучшенный вариант с более высоким уровнем сервиса.",
                price_extra=120,
            )
            TourHotel.objects.create(
                tour=tour,
                name=f"{city_name} Family Hotel 4*",
                description="Уютный вариант для семейного и спокойного отдыха.",
                price_extra=80,
            )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Успешно обновлено {tours.count()} туров с деталями, днями и отелями!")
        )