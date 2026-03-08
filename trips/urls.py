from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet, ExpenseViewSet, BudgetViewSet

router = DefaultRouter()
router.register(r"trips", TripViewSet, basename="trips")
router.register(r"expenses", ExpenseViewSet, basename="expenses")
router.register(r"budget", BudgetViewSet, basename="budget")  # ← НОВОЕ!

urlpatterns = [
    path("", include(router.urls)),
]