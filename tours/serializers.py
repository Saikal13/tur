from rest_framework import serializers
from .models import Country, Tour


class CountrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    tours_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "description",
            "image",
            "owner",
            "visa_free",       # ✅ новое
            "vacation_type",   # ✅ новое
            "tours_count",
        ]


class TourSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    country_name = serializers.ReadOnlyField(source="country.name")
    end_date = serializers.ReadOnlyField()

    class Meta:
        model = Tour
        fields = [
            "id",
            "title",
            "country",
            "country_name",
            "description",
            "price",
            "difficulty",
            "departure_city",  # ✅ новое
            "max_slots",
            "start_date",
            "duration_days",
            "end_date",
            "owner",
            "created_at",
        ]