from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime
from bookings.models import BookingRequest
from .models import TourNotification


@receiver(post_save, sender=BookingRequest)
def send_tour_notification(sender, instance, created, update_fields, **kwargs):
    """
    Отправляет уведомление клиенту при смене статуса на 'confirmed' или 'done'
    """

    # Проверяем изменился ли статус и стал ли он 'confirmed' или 'done'
    if update_fields and 'status' in update_fields:
        if instance.status in ['confirmed', 'done']:  # ✅ ОБА СТАТУСА!
            send_confirmation_email(instance)


def send_confirmation_email(booking):
    """
    Отправляет email с деталями вылета клиенту
    """
    try:
        tour = booking.tour

        # Формируем контекст для письма
        context = {
            'client_name': booking.name,
            'tour_title': tour.title,
            'country': tour.country.name,
            'phone': booking.phone,
            'email': booking.email,
            'price': booking.price,
            'currency': booking.currency,
            'created_date': booking.created_at.strftime('%d.%m.%Y'),
            'confirmation_date': datetime.now().strftime('%d.%m.%Y %H:%M'),
        }

        # Если у тура есть дата старта - добавляем её
        if hasattr(tour, 'start_date') and tour.start_date:
            context['departure_date'] = tour.start_date.strftime('%d.%m.%Y')

        if hasattr(tour, 'start_time') and tour.start_time:
            context['departure_time'] = tour.start_time.strftime('%H:%M')

        # Формируем текст письма
        subject = f"✅ Ваш тур подтвержден! {tour.country.name} - {tour.title}"

        html_message = render_to_string('notification_email.html', context)

        # Отправляем письмо
        send_mail(
            subject=subject,
            message='Ваш тур подтвержден!',  # Plain text версия
            from_email='noreply@touristplatform.com',
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=True,
        )

        # Сохраняем в БД что уведомление отправлено
        TourNotification.objects.create(
            booking=booking,
            country=tour.country.name,
            departure_date=tour.start_date if hasattr(tour, 'start_date') else timezone.now().date(),
            departure_time=tour.start_time if hasattr(tour, 'start_time') else timezone.now().time(),
            is_sent=True,
            sent_at=timezone.now(),
        )

    except Exception as e:
        print(f"Ошибка при отправке email: {e}")