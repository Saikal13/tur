from datetime import date

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from trips.models import Trip
from tours.models import Tour
from info.models import Country
from django.contrib.auth.models import User


def register_page(request):
    """Страница регистрации"""
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
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Админы идут в админ-панель
            if user.is_staff or user.is_superuser:
                return redirect('/admin-panel/')

            # Обычные пользователи на главную
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'auth/login.html')


def logout_page(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('login_page')


@login_required(login_url="/login/")
def home(request):
    """Главная страница"""
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

    # ✅ НОВОЕ: Страны с новостями и фактами
    countries_with_info = Country.objects.prefetch_related(
        'news', 'facts', 'attractions', 'events'
    )[:6]

    # ✅ НОВОЕ: Уведомления
    try:
        from notifications.models import TourNotification
        unread_count = TourNotification.objects.filter(is_read=False).count()
    except:
        unread_count = 0

    context = {
        "popular_tours": popular_tours,
        "next_trip": next_trip,
        "days_to_start": days_to_start,
        "countries_with_info": countries_with_info,  # ✅ НОВОЕ
        "unread_count": unread_count,  # ✅ НОВОЕ
    }
    return render(request, "home.html", context)


@login_required(login_url="/login/")
def api_page(request):
    """API страница"""
    return render(request, "api_page.html")