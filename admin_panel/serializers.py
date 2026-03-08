from rest_framework import serializers
from bookings.models import BookingRequest
from django.contrib.auth.models import User
from tours.models import Tour
from .models import AdminLog, AdminComment


class AdminLogSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin.username', read_only=True)

    class Meta:
        model = AdminLog
        fields = ['id', 'admin', 'admin_username', 'booking', 'action', 'old_value', 'new_value', 'created_at']
        read_only_fields = ['created_at']


class AdminCommentSerializer(serializers.ModelSerializer):
    admin_username = serializers.CharField(source='admin.username', read_only=True)

    class Meta:
        model = AdminComment
        fields = ['id', 'booking', 'admin', 'admin_username', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BookingRequestDetailSerializer(serializers.ModelSerializer):
    comments = AdminCommentSerializer(source='admin_comments', many=True, read_only=True)
    logs = AdminLogSerializer(source='admin_logs', many=True, read_only=True)
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = BookingRequest
        fields = [
            'id', 'name', 'phone', 'email', 'tour', 'tour_title',
            'status', 'status_display', 'comment', 'comments', 'logs',
            'created_at'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class TourSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'title', 'price', 'country', 'country_name', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']