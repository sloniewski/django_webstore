from django import template
from django.conf import settings
from iso4217 import Currency

register = template.Library()


@register.filter()
def product_price(value, arg=None):

    if arg is None:
        currency = Currency(settings.DEFAULT_PRICE_CURRENCY)
    else:
        currency = Currency(arg)

    if value is not None:
        return str(value) + ' ' + currency.code
    else:
        return '--.-- ' + currency.code
