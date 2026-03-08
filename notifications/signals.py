from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import time
from bookings.models import BookingRequest

try:
    from .models import TourNotification
except ImportError:
    TourNotification = None

print("Notifications signals loaded!")


@receiver(post_save, sender=BookingRequest)
def create_notification_for_user(sender, instance, created, update_fields, **kwargs):
    """
    Создаёт уведомление когда статус меняется на 'confirmed' или 'done'
    Уведомление видно ТОЛЬКО пользователю чья заявка!
    """

    if update_fields is None or 'status' in update_fields:
        if instance.status in ['confirmed', 'done']:

            try:
                if not TourNotification:
                    print("TourNotification model not found")
                    return

                # Проверяем не создано ли уже
                existing = TourNotification.objects.filter(booking=instance).exists()
                if existing:
                    print(f"Notification already exists for booking {instance.id}")
                    return

                tour = instance.tour

                # Создаём уведомление ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
                notification = TourNotification.objects.create(
                    booking=instance,
                    country=tour.country.name if tour.country else "Not specified",
                    departure_date=tour.start_date if hasattr(tour,
                                                              'start_date') and tour.start_date else timezone.now().date(),
                    departure_time=tour.start_time if hasattr(tour, 'start_time') and tour.start_time else time(10, 0),
                    is_sent=False,
                    sent_at=None,
                )

                print(f"\n=== NOTIFICATION CREATED FOR USER ===")
                print(f"Notification ID: {notification.id}")
                print(f"User Email: {instance.email}")
                print(f"User Name: {instance.name}")
                print(f"Country: {notification.country}")
                print(f"Status: {instance.status}")
                print(f"======================================\n")

            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()