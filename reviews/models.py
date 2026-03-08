from django.db import models
from django.contrib.auth.models import User
from tours.models import Tour


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tour")

    def __str__(self):
        return f"{self.user.username} -> {self.tour.title} ({self.rating})"