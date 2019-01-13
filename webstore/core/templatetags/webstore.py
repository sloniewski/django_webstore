from decimal import Decimal, ROUND_DOWN

from django import template

register = template.Library()


@register.filter
def round(value):
    dec = Decimal(value)
    return dec.quantize(Decimal('.01'), rounding=ROUND_DOWN)
