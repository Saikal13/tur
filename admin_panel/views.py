from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from bookings.models import BookingRequest
from tours.models import Tour
from .models import AdminLog, AdminComment
from django.db.models.functions import TruncDate


def is_admin(user):
    """Проверка, что пользователь админ"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    """Главная панель администратора"""

    # Статистика
    total_bookings = BookingRequest.objects.count()
    new_bookings = BookingRequest.objects.filter(status='new').count()
    in_progress = BookingRequest.objects.filter(status='in_progress').count()
    confirmed = BookingRequest.objects.filter(status='confirmed').count()
    cancelled = BookingRequest.objects.filter(status='cancelled').count()

    total_users = User.objects.count()
    total_tours = Tour.objects.count()

    # Последние заявки
    recent_bookings = BookingRequest.objects.all()[:10]

    context = {
        'total_bookings': total_bookings,
        'new_bookings': new_bookings,
        'in_progress': in_progress,
        'confirmed': confirmed,
        'cancelled': cancelled,
        'total_users': total_users,
        'total_tours': total_tours,
        'recent_bookings': recent_bookings,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def bookings_list(request):
    """Список всех заявок"""

    bookings = BookingRequest.objects.all().order_by('-created_at')

    # Поиск
    search = request.GET.get('search', '')
    if search:
        bookings = bookings.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )

    # Фильтр по статусу
    status = request.GET.get('status', '')
    if status:
        bookings = bookings.filter(status=status)

    # Сортировка
    ordering = request.GET.get('ordering', '-created_at')
    allowed_orderings = ['-created_at', 'created_at', '-id', 'name']
    if ordering in allowed_orderings:
        bookings = bookings.order_by(ordering)

    context = {
        'bookings': bookings,
        'search': search,
        'status': status,
        'ordering': ordering,
        'status_choices': BookingRequest.STATUS_CHOICES,
    }

    return render(request, 'admin_bookings_list.html', context)


@login_required
@user_passes_test(is_admin)
def booking_detail(request, pk):
    """Детали заявки"""

    booking = get_object_or_404(BookingRequest, pk=pk)
    comments = booking.admin_comments.all()
    logs = booking.admin_logs.all()

    if request.method == 'POST':
        # Изменение статуса
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in BookingRequest.STATUS_CHOICES]:
            old_status = booking.status
            booking.status = new_status
            booking.save()

            # Логирование
            AdminLog.objects.create(
                admin=request.user,
                booking=booking,
                action='status_changed',
                old_value=old_status,
                new_value=new_status,
            )

            messages.success(request, f"Статус изменён с '{old_status}' на '{new_status}'")

        # Добавление комментария
        comment_text = request.POST.get('comment')
        if comment_text:
            AdminComment.objects.create(
                booking=booking,
                admin=request.user,
                comment=comment_text,
            )

            # Логирование
            AdminLog.objects.create(
                admin=request.user,
                booking=booking,
                action='comment_added',
                new_value=comment_text[:100],
            )

            messages.success(request, "Комментарий добавлен")

        return redirect('booking_detail', pk=pk)

    context = {
        'booking': booking,
        'comments': comments,
        'logs': logs,
        'status_choices': BookingRequest.STATUS_CHOICES,
    }

    return render(request, 'admin_booking_detail.html', context)


@login_required
@user_passes_test(is_admin)
def users_list(request):
    """Список пользователей"""

    users = User.objects.all().order_by('-date_joined')

    # Поиск
    search = request.GET.get('search', '')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search)
        )

    # Фильтр по типу
    user_type = request.GET.get('type', '')
    if user_type == 'staff':
        users = users.filter(is_staff=True)
    elif user_type == 'active':
        users = users.filter(is_active=True)
    elif user_type == 'inactive':
        users = users.filter(is_active=False)

    context = {
        'users': users,
        'search': search,
        'user_type': user_type,
    }

    return render(request, 'admin_users_list.html', context)


@login_required
@user_passes_test(is_admin)
def tours_list(request):
    """Список туров"""

    tours = Tour.objects.all().order_by('-created_at')

    # Поиск
    search = request.GET.get('search', '')
    if search:
        tours = tours.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # Фильтр по стране
    country = request.GET.get('country', '')
    if country:
        tours = tours.filter(country__name__icontains=country)

    # Фильтр по статусу
    active = request.GET.get('active', '')
    if active == 'true':
        tours = tours.filter(is_active=True)
    elif active == 'false':
        tours = tours.filter(is_active=False)

    context = {
        'tours': tours,
        'search': search,
        'country': country,
        'active': active,
    }

    return render(request, 'admin_tours_list.html', context)


@login_required
@user_passes_test(is_admin)
def stats(request):
    """Статистика"""

    # По статусам
    stats_by_status = BookingRequest.objects.values('status').annotate(count=Count('id'))

    # По турам
    stats_by_tour = BookingRequest.objects.values('tour__title').annotate(count=Count('id')).order_by('-count')[:10]

    # По дням
    stats_by_date = BookingRequest.objects.annotate(date=TruncDate('created_at')).values('date').annotate(
        count=Count('id')).order_by('-date')[:30]

    context = {
        'stats_by_status': stats_by_status,
        'stats_by_tour': stats_by_tour,
        'stats_by_date': stats_by_date,
    }

    return render(request, 'admin_stats.html', context)