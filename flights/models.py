from django.conf import settings
from django.db import models
from django.utils import timezone


class Airport(models.Model):
    """
    Справочник аэропортов (можно заполнять вручную/скриптом).
    IATA: SVO, IST, DXB и т.д.
    """
    iata = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=180)
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["iata"]

    def __str__(self):
        return f"{self.iata} — {self.name}"


class FlightSearchQuery(models.Model):
    """
    Лог запросов (чтобы видеть, что ищут пользователи; можно показывать историю).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    origin = models.CharField(max_length=3)      # IATA
    destination = models.CharField(max_length=3) # IATA
    depart_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    adults = models.PositiveSmallIntegerField(default=1)
    children = models.PositiveSmallIntegerField(default=0)
    cabin = models.CharField(max_length=16, default="ECONOMY")  # ECONOMY/BUSINESS...

    def __str__(self):
        rt = f" -> {self.return_date}" if self.return_date else ""
        return f"{self.origin}-{self.destination} {self.depart_date}{rt}"


class FlightOfferCache(models.Model):
    """
    Кэш офферов (результатов поиска) чтобы не дергать API постоянно.
    Сохраняем "сырой" JSON.
    """
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    depart_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    adults = models.PositiveSmallIntegerField(default=1)
    cabin = models.CharField(max_length=16, default="ECONOMY")

    provider = models.CharField(max_length=40, default="stub")  # amadeus/kiwi/stub
    payload = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["origin", "destination", "depart_date", "return_date", "adults", "cabin"]),
            models.Index(fields=["expires_at"]),
        ]

    def is_valid(self):
        return self.expires_at > timezone.now()