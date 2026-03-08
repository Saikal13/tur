from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import action

from .models import Trip, Expense
from .serializers import TripSerializer, ExpenseSerializer
from .forms import TripForm, ExpenseForm


def _build_dashboard_context(user):
    trips = (
        Trip.objects.filter(user=user)
        .prefetch_related("expenses")
        .order_by("-created_at")
    )

    expenses = (
        Expense.objects.filter(trip__user=user)
        .select_related("trip")
        .order_by("-date", "-id")
    )

    total_spent = expenses.aggregate(total_spent=Sum("amount"))["total_spent"] or 0
    total_budget = sum((t.budget for t in trips), start=0)

    trip_form = TripForm()
    expense_form = ExpenseForm()
    expense_form.fields["trip"].queryset = Trip.objects.filter(user=user).order_by("-created_at")

    return {
        "trips": trips,
        "expenses": expenses,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "trip_form": trip_form,
        "expense_form": expense_form,
    }


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "trips_dashboard.html"

    def get_queryset(self):
        return (
            Trip.objects.filter(user=self.request.user)
            .prefetch_related("expenses")
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        # HTML в браузере
        accept = request.META.get("HTTP_ACCEPT", "")
        if "text/html" in accept and request.GET.get("format") != "json":
            context = _build_dashboard_context(request.user)
            return Response(context, template_name=self.template_name)

        # JSON API
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Если это API JSON — оставляем стандартное поведение
        if request.GET.get("format") == "json" or request.content_type == "application/json":
            return super().create(request, *args, **kwargs)

        action = request.POST.get("action")

        if action == "create_trip":
            form = TripForm(request.POST)
            if form.is_valid():
                trip = form.save(commit=False)
                trip.user = request.user
                trip.save()
                messages.success(request, "✅ Поездка создана!")
                return redirect(request.path)

            messages.error(request, "❌ Проверь поля поездки.")
            context = _build_dashboard_context(request.user)
            context["trip_form"] = form
            return Response(context, template_name=self.template_name, status=status.HTTP_200_OK)

        if action == "create_expense":
            form = ExpenseForm(request.POST)
            form.fields["trip"].queryset = Trip.objects.filter(user=request.user).order_by("-created_at")

            if form.is_valid():
                expense = form.save(commit=False)

                if expense.trip.user_id != request.user.id:
                    messages.error(request, "❌ Нельзя добавлять расход в чужую поездку.")
                else:
                    expense.save()
                    messages.success(request, "✅ Расход добавлен!")

                return redirect(request.path)

            messages.error(request, "❌ Проверь поля расхода.")
            context = _build_dashboard_context(request.user)
            context["expense_form"] = form
            return Response(context, template_name=self.template_name, status=status.HTTP_200_OK)

        messages.error(request, "❌ Неизвестное действие.")
        return redirect(request.path)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(trip__user=self.request.user).order_by("-date", "-id")


# ========== НОВЫЙ ViewSet для бюджета ==========
class BudgetViewSet(viewsets.ViewSet):
    """Эндпоинт для работы с бюджетом путешествия"""
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def list(self, request):
        """Получить список всех поездок с бюджетом"""
        trips = Trip.objects.filter(user=request.user).prefetch_related("expenses").order_by("-created_at")

        budget_data = []
        for trip in trips:
            total_expenses = trip.total_expenses
            remaining = float(trip.budget) - float(total_expenses)
            percentage = 0
            if trip.budget > 0:
                percentage = (float(total_expenses) / float(trip.budget)) * 100

            budget_data.append({
                'id': trip.id,
                'title': trip.title,
                'budget': trip.budget,
                'total_expenses': total_expenses,
                'remaining': remaining,
                'percentage': round(percentage, 2),
                'start_date': trip.start_date,
                'end_date': trip.end_date,
                'expenses_count': trip.expenses.count(),
            })

        context = {
            'budget_data': budget_data,
            'total_budget': sum(float(t['budget']) for t in budget_data),
            'total_spent': sum(float(t['total_expenses']) for t in budget_data),
        }

        # Если JSON API
        if request.GET.get("format") == "json":
            return Response(context)

        # Если HTML
        return Response(context, template_name="budget.html")

    def retrieve(self, request, pk=None):
        """Получить бюджет конкретной поездки"""
        trip = get_object_or_404(Trip, pk=pk, user=request.user)

        total_expenses = trip.total_expenses
        remaining = float(trip.budget) - float(total_expenses)
        percentage = 0
        if trip.budget > 0:
            percentage = (float(total_expenses) / float(trip.budget)) * 100

        expenses = trip.expenses.all().order_by('-date')

        context = {
            'trip': trip,
            'budget': trip.budget,
            'total_expenses': total_expenses,
            'remaining': remaining,
            'percentage': round(percentage, 2),
            'expenses': expenses,
            'is_over_budget': total_expenses > trip.budget,
        }

        # Если JSON API
        if request.GET.get("format") == "json":
            return Response(context)

        # Если HTML
        return Response(context, template_name="trip_budget.html")


@login_required
def trips_page(request):
    context = _build_dashboard_context(request.user)
    return render(request, "trips_dashboard.html", context)