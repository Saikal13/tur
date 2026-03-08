from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.text import slugify


class Country(models.Model):
    VACATION_CHOICES = [
        ("any", "Любой"),
        ("sea", "Море"),
        ("mountains", "Горы"),
        ("city", "Город"),
        ("ski", "Горнолыжный"),
        ("excursion", "Экскурсионный"),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True)

    description = models.TextField(blank=True)
    image = models.URLField(blank=True, default="")

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="countries",
        null=True,
        blank=True,
    )

    visa_free = models.BooleanField(default=False)

    vacation_type = models.CharField(
        max_length=20,
        choices=VACATION_CHOICES,
        default="any",
    )

    about = models.TextField(blank=True, default="")
    short_info = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("country", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.country.name}"


class Tour(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Легкий"),
        ("medium", "Средний"),
        ("hard", "Сложный"),
    ]

    DEPARTURE_CITY_CHOICES = [
        ("bishkek", "Бишкек"),
        ("osh", "Ош"),
        ("almaty", "Алматы"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)

    description = models.TextField()

    image = models.URLField(
        blank=True,
        default="https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="easy"
    )

    start_date = models.DateField()
    duration_days = models.PositiveIntegerField()

    max_slots = models.PositiveIntegerField(default=15)

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="tours"
    )

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tours",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tours",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    departure_city = models.CharField(
        max_length=20,
        choices=DEPARTURE_CITY_CHOICES,
        default="bishkek",
    )

    is_active = models.BooleanField(default=True)

    # ===== НОВЫЕ ПОЛЯ =====
    hotel_name = models.CharField(max_length=150, blank=True, default="")
    departure_time = models.TimeField(null=True, blank=True)
    details = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.duration_days)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.country.name})"


class TourDay(models.Model):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="days"
    )
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=150, blank=True, default="")
    description = models.TextField()

    class Meta:
        ordering = ["day_number"]
        unique_together = ("tour", "day_number")

    def __str__(self):
        return f"{self.tour.title} — День {self.day_number}"


class TourHotel(models.Model):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="hotels"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default="")
    price_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.tour.title}"