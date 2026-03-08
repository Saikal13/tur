from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

from tours.models import Tour, Country

fake = Faker("ru_RU")

COUNTRY_NAMES = [
    "Италия", "Франция", "Испания", "Турция", "Грузия", "ОАЭ",
    "Таиланд", "Япония", "Исландия", "Норвегия", "Греция", "Португалия",
    "Швейцария", "Австрия", "Чехия"
]

DIFFICULTIES = ["easy", "medium", "hard"]


class Command(BaseCommand):
    help = "Seed tours with demo data"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=300)

    def handle(self, *args, **options):
        count = options["count"]
        now = timezone.now().date()

        # создаём страны
        for name in COUNTRY_NAMES:
            Country.objects.get_or_create(
                name=name,
                defaults={"description": f"Описание страны {name}"},
            )

        countries = list(Country.objects.all())
        if not countries:
            self.stdout.write(self.style.ERROR("❌ Countries not found"))
            return

        tours = []
        for i in range(count):
            country_obj = random.choice(countries)
            duration = random.choice([3, 5, 7, 10, 14])
            start_date = now + timedelta(days=random.randint(1, 240))

            title = f"{fake.word().capitalize()} тур в {country_obj.name} • {duration} дней"

            tours.append(
                Tour(
                    title=title,
                    description=fake.paragraph(nb_sentences=4),
                    price=round(random.uniform(150, 3000), 2),
                    difficulty=random.choice(DIFFICULTIES),
                    start_date=start_date,
                    duration_days=duration,
                    max_slots=random.randint(10, 40),
                    country=country_obj,
                )
            )

        Tour.objects.bulk_create(tours, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {count} tours"))