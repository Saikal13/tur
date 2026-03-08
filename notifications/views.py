from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookings.models import BookingRequest
from .models import TourNotification


@login_required
def my_notifications(request):
    """
    Показывает ТОЛЬКО уведомления текущего пользователя!
    Сайкал видит свои, kak видит свои
    """

    # Получаем email текущего пользователя
    user_email = request.user.email

    # Если email пуст - показываем пустую страницу
    if not user_email:
        notifications = TourNotification.objects.none()
        confirmed_bookings = BookingRequest.objects.none()
    else:
        # ФИЛЬТРУем ТОЛЬКО по email текущего пользователя
        notifications = TourNotification.objects.filter(
            booking__email=user_email
        ).order_by('-created_at')

        confirmed_bookings = BookingRequest.objects.filter(
            email=user_email,
            status__in=['confirmed', 'done']
        ).order_by('-created_at')

    # Отмечаем как прочитанные
    if notifications:
        TourNotification.objects.filter(
            booking__email=user_email,
            is_read=False
        ).update(is_read=True)

    context = {
        'notifications': notifications,
        'bookings': confirmed_bookings,
        'total_count': notifications.count(),
        'user_email': user_email,
    }

    return render(request, 'my_notifications.html', context)


@login_required
def notification_detail(request, notification_id):
    """
    Детальная страница уведомления
    Только если это уведомление текущего пользователя!
    """
    notification = get_object_or_404(TourNotification, id=notification_id)

    # ПРОВЕРЯЕМ что это уведомление для текущего пользователя
    if notification.booking.email != request.user.email:
        return render(request, '404.html', status=403)

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