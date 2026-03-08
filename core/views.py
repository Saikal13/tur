from datetime import date

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from trips.models import Trip
from tours.models import Tour


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "auth/register.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})


@login_required(login_url="/login/")
def home(request):
    # Популярные туры (последние 6)
    popular_tours = Tour.objects.all().order_by("-id")[:6]

    # Ближайшая поездка текущего юзера
    today = date.today()
    next_trip = (
        Trip.objects.filter(user=request.user, start_date__gte=today)
        .order_by("start_date")
        .first()
    )

    days_to_start = None
    if next_trip:
        days_to_start = (next_trip.start_date - today).days

    context = {
        "popular_tours": popular_tours,
        "next_trip": next_trip,
        "days_to_start": days_to_start,
    }
    return render(request, "home.html", context)


@login_required(login_url="/login/")
def api_page(request):
    return render(request, "api_page.html")