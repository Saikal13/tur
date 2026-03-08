from django.db import models
from tours.models import Country


class News(models.Model):
    """Новости о странах и туризме"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('museum', 'Музей'),
            ('nature', 'Природа'),
            ('event', 'Событие'),
            ('other', 'Другое'),
        ],
        default='other'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.country.name}"


class CountryFact(models.Model):
    """Интересные факты о странах"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='facts')
    fact = models.TextField()
    fact_type = models.CharField(
        max_length=50,
        choices=[
            ('historical', 'Исторический'),
            ('geographical', 'Географический'),
            ('cultural', 'Культурный'),
            ('other', 'Другое'),
        ],
        default='other'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.country.name} - {self.fact[:50]}"


class Attraction(models.Model):
    """Интересные места в стране"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=255)
    description = models.TextField()
    attraction_type = models.CharField(
        max_length=50,
        choices=[
            ('museum', 'Музей'),
            ('monument', 'Памятник'),
            ('park', 'Парк'),
            ('church', 'Церковь'),
            ('nature', 'Природа'),
            ('other', 'Другое'),
        ],
        default='other'
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    rating = models.FloatField(default=0, help_text="Рейтинг от 0 до 5")
    image = models.ImageField(upload_to='attractions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return f"{self.name} ({self.country.name})"


class Event(models.Model):
    """События и мероприятия в стране"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('festival', 'Фестиваль'),
            ('exhibition', 'Выставка'),
            ('concert', 'Концерт'),
            ('sport', 'Спорт'),
            ('other', 'Другое'),
        ],
        default='other'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    rating = models.FloatField(default=0, help_text="Рейтинг от 0 до 5")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} ({self.country.name})"