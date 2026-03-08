from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from bookings.models import BookingRequest

# ✅ ИМПОРТИРУЕМ ИЗ admin_panel
from admin_panel.models import AdminComment, AdminLog

# ✅ ИМПОРТИРУЕМ ИЗ client_panel.models
try:
    from .models import ClientResponse
except ImportError:
    ClientResponse = None


@login_required
def booking_status(request, booking_id):
    """
    Страница статуса заявки для клиента
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
    }

    return render(request, 'client_booking_status.html', context)


def booking_status_public(request, booking_id, email):
    """
    Открытая страница статуса заявки (без логина)
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
def get_new_messages(request):
    """
    AJAX endpoint для получения новых комментариев
    Возвращает JSON с новыми сообщениями
    """
    # Получаем timestamp последнего загруженного сообщения (если есть)
    last_timestamp = request.GET.get('last_timestamp', None)

    # Получаем все комментарии
    all_comments = AdminComment.objects.all().order_by('-created_at')

    # Если есть timestamp - берём только новые
    if last_timestamp:
        from django.utils import timezone
        from datetime import datetime
        try:
            last_dt = datetime.fromisoformat(last_timestamp)
            all_comments = all_comments.filter(created_at__gt=last_dt)
        except:
            pass

    # Формируем JSON ответ
    messages = []
    for comment in all_comments:
        messages.append({
            'id': comment.id,
            'booking_id': comment.booking.id,
            'booking_name': comment.booking.name,
            'admin_name': comment.admin.username,
            'comment': comment.comment,
            'created_at': comment.created_at.isoformat(),
            'is_read': comment.is_read,
        })

    # Подсчитываем непрочитанные
    unread_count = AdminComment.objects.filter(is_read=False).count()

    return JsonResponse({
        'messages': messages,
        'unread_count': unread_count,
        'success': True,
    })


@login_required
@require_http_methods(["POST"])
def send_client_response(request):
    """
    AJAX endpoint для отправки ответа клиента
    """
    booking_id = request.POST.get('booking_id')
    message = request.POST.get('message', '').strip()

    if not booking_id or not message:
        return JsonResponse({'success': False, 'error': 'Заполни все поля'})

    try:
        booking = BookingRequest.objects.get(id=booking_id)

        # Создаём ответ клиента
        if ClientResponse:
            response = ClientResponse.objects.create(
                booking=booking,
                message=message
            )

            return JsonResponse({
                'success': True,
                'message': 'Ответ отправлен! Администратор увидит его вскоре.',
                'response_id': response.id
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Модель ClientResponse не найдена'
            })

    except BookingRequest.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Заявка не найдена'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def mark_messages_as_read(request):
    """
    Отметить все сообщения как прочитанные
    """
    if request.method == 'POST':
        AdminComment.objects.filter(is_read=False).update(is_read=True)
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