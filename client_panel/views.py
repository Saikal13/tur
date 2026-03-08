from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from bookings.models import BookingRequest
from admin_panel.models import AdminComment, AdminLog


@login_required
def booking_status(request, booking_id):
    """
    Страница статуса заявки для клиента
    """
    # Клиент видит только свою заявку по email
    booking = get_object_or_404(BookingRequest, id=booking_id, email=request.GET.get('email', ''))

    comments = booking.admin_comments.all()
    logs = booking.admin_logs.all()

    context = {
        'booking': booking,
        'comments': comments,
        'logs': logs,
    }

    return render(request, 'client_booking_status.html', context)


def booking_status_public(request, booking_id, email):
    """
    Открытая страница статуса заявки (без логина)
    Доступна по ссылке с email верификацией
    """
    try:
        booking = BookingRequest.objects.get(id=booking_id)
    except BookingRequest.DoesNotExist:
        return render(request, '404.html', status=404)

    comments = booking.admin_comments.all()
    logs = booking.admin_logs.all()

    context = {
        'booking': booking,
        'comments': comments,
        'logs': logs,
        'is_public': True,
    }

    return render(request, 'client_booking_status.html', context)


@login_required
def client_messages(request):
    """
    Страница всех сообщений клиента от администратора
    Показывает ВСЕ комментарии (не фильтруем по email)
    """
    # Получаем ВСЕ заявки
    bookings = BookingRequest.objects.all().order_by('-created_at')

    # Получаем ВСЕ комментарии БЕЗ фильтра по email
    all_comments = AdminComment.objects.all().order_by('-created_at')

    # Подсчитываем непрочитанные сообщения ДО slice
    unread_count = all_comments.filter(is_read=False).count()

    # Теперь берём последние 20 комментариев
    comments = all_comments[:20]

    context = {
        'bookings': bookings,
        'comments': comments,
        'unread_count': unread_count,
    }

    return render(request, 'client_messages.html', context)


@login_required
def client_messages_count(request):
    """
    AJAX endpoint для получения количества новых сообщений
    """
    user_email = request.user.email
    bookings = BookingRequest.objects.filter(email=user_email).values_list('id', flat=True)
    unread = AdminComment.objects.filter(
        booking_id__in=bookings,
        is_read=False
    ).count()

    return JsonResponse({'unread_count': unread})


@login_required
def mark_messages_as_read(request):
    """
    Отметить все сообщения как прочитанные
    """
    if request.method == 'POST':
        user_email = request.user.email
        bookings = BookingRequest.objects.filter(email=user_email).values_list('id', flat=True)

        AdminComment.objects.filter(
            booking_id__in=bookings,
            is_read=False
        ).update(is_read=True)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def client_messages_public(request, email):
    """
    Открытая страница сообщений (для ссылки из письма)
    """
    bookings = BookingRequest.objects.filter(email=email).order_by('-created_at')
    booking_ids = bookings.values_list('id', flat=True)
    comments = AdminComment.objects.filter(booking_id__in=booking_ids).order_by('-created_at')

    context = {
        'bookings': bookings,
        'comments': comments,
        'is_public': True,
        'user_email': email,
    }

    return render(request, 'client_messages.html', context)