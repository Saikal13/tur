from django import forms


CABIN_CHOICES = [
    ("ECONOMY", "Эконом"),
    ("BUSINESS", "Бизнес"),
    ("FIRST", "Первый"),
]


class FlightSearchForm(forms.Form):
    origin = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={
            "class": "field",
            "placeholder": "SVO",
        })
    )

    destination = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={
            "class": "field",
            "placeholder": "IST",
        })
    )

    depart_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "field",
        })
    )

    return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "field",
        })
    )

    adults = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            "class": "field",
        })
    )

    children = forms.IntegerField(
        min_value=0,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "field",
        })
    )

    cabin = forms.ChoiceField(
        choices=CABIN_CHOICES,
        widget=forms.Select(attrs={
            "class": "field",
        })
    )

    def clean_origin(self):
        v = (self.cleaned_data.get("origin") or "").strip().upper()
        if len(v) != 3:
            raise forms.ValidationError("Введите IATA код из 3 букв (например SVO).")
        return v

    def clean_destination(self):
        v = (self.cleaned_data.get("destination") or "").strip().upper()
        if len(v) != 3:
            raise forms.ValidationError("Введите IATA код из 3 букв (например IST).")
        return v