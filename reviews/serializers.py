from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tour_title = serializers.CharField(source="tour.title", read_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "tour",
            "tour_title",
            "rating",
            "comment",
            "photo",
            "created_at",
        ]
        read_only_fields = ["id", "user", "tour_title", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        tour = attrs.get("tour")

        if request and request.user and request.user.is_authenticated:
            if self.instance is None and Review.objects.filter(user=request.user, tour=tour).exists():
                raise serializers.ValidationError({
                    "non_field_errors": ["Вы уже оставили отзыв на этот тур."]
                })

        return attrs