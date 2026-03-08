from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from bookings.models import BookingRequest


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def dashboard_home(request):
    requests = BookingRequest.objects.all().order_by("-created_at")
    return render(request, "dashboard/home.html", {"requests": requests})