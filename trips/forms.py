from django import forms
from .models import Trip, Expense

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ("title", "start_date", "end_date", "budget")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("trip", "title", "amount", "date")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }