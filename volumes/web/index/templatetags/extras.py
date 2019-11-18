from django.template import Library
from decimal import Decimal

# Filters
register = Library()


@register.filter
def divide(value, arg):
    try:
        return Decimal(Decimal(value) / Decimal(arg)).normalize()

    except Exception:
        pass

    return 0


@register.filter
def status_colors(tag):
    if tag == "success":
        return "green darken-1 white-text"

    if tag == 'error':
        return 'red darken-4 white-text'

    if tag == 'info':
        return 'blue white-text'

    return 'amber accent-1 grey-text text-darken-4'


@register.filter
def text_colors(tag):
    if tag == "success":
        return "white-text"

    if tag == 'error':
        return 'white-text'

    if tag == 'info':
        return 'white-text'

    return 'grey-text text-darken-4'
