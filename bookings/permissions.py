from rest_framework.permissions import BasePermission


class IsOwnerThroughTrip(BasePermission):
    """
    Доступ только к бронированиям, принадлежащим пользователю через tour.user
    """

    def has_object_permission(self, request, view, obj):
        return obj.tour.user_id == request.user.id