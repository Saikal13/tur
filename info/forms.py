from django import forms
from .models import News, CountryFact, Attraction, Event

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'image']

class CountryFactForm(forms.ModelForm):
    class Meta:
        model = CountryFact
        fields = ['fact', 'fact_type']