from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from bookings.models import BookingRequest

try:
    from .models import TourNotification
except ImportError:
    TourNotification = None

print("Signals loaded!")


@receiver(post_save, sender=BookingRequest)
def create_tour_notification(sender, instance, created, update_fields, **kwargs):
    if update_fields is None or 'status' in update_fields:
        if instance.status in ['confirmed', 'done']:
            print(f"\nSignal triggered! Status: {instance.status}")

            try:
                if not TourNotification:
                    print("TourNotification model not found")
                    return

                existing = TourNotification.objects.filter(booking=instance).exists()
                if existing:
                    print("Notification already exists")
                    return

                tour = instance.tour

                notification = TourNotification.objects.create(
                    booking=instance,
                    country=tour.country.name if tour.country else "Not specified",
                    departure_date=tour.start_date if hasattr(tour,
                                                              'start_date') and tour.start_date else timezone.now().date(),
                    departure_time=tour.start_time if hasattr(tour,
                                                              'start_time') and tour.start_time else timezone.now().time(),
                    is_sent=False,
                    sent_at=None,
                )

                print(f"Notification created! ID: {notification.id}")
                print(f"   Country: {notification.country}")
                print(f"   Date: {notification.departure_date}")
                print(f"   Passenger: {instance.name}\n")

            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()