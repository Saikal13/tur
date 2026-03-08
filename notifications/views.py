from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from bookings.models import BookingRequest
from .models import TourNotification


@login_required
def my_notifications(request):
    """
    Страница со всеми уведомлениями клиента о подтвержденных турах
    """

    # ✅ ИСПРАВЛЕНО: показываем ВСЕ уведомления (для демо)
    # В реальном проекте фильтруй по email или по юзеру
    notifications = TourNotification.objects.all().order_by('-created_at')

    confirmed_bookings = BookingRequest.objects.filter(
        status__in=['confirmed', 'done']
    ).order_by('-created_at')

    # Отмечаем как прочитанные
    if notifications:
        TourNotification.objects.filter(
            is_read=False
        ).update(is_read=True)

    context = {
        'notifications': notifications,
        'bookings': confirmed_bookings,
        'total_count': notifications.count(),
    }

    return render(request, 'my_notifications.html', context)


@login_required
def notification_detail(request, notification_id):
    """
    Детальная страница уведомления о туре
    """
    notification = get_object_or_404(TourNotification, id=notification_id)

    # Отмечаем как прочитанное
    notification.is_read = True
    notification.save()

    booking = notification.booking
    tour = booking.tour

    context = {
        'notification': notification,
        'booking': booking,
        'tour': tour,
    }

    return render(request, 'notification_detail.html', context)