from django import template

register = template.Library()


@register.filter
def min_value(value, arg):
    """Возвращает минимальное значение между value и arg"""
    try:
        return min(float(value), float(arg))
    except (ValueError, TypeError):
        return value


@register.filter
def abs_value(value):
    """Возвращает абсолютное значение"""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return value