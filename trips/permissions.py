from rest_framework.permissions import BasePermission


class IsOwnerTrip(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerExpense(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.trip.user == request.user