from django.db import models

from webstore.order.models import Order
from webstore.cash.fields import CashField
from webstore.delivery.managers import (
    DeliveryPriceManager,
    DeliveryManager,
)


class DeliveryOption(models.Model):
    """
    Can represent a courier/post or other shipping
    """
    objects = DeliveryManager()

    name = models.CharField(
        max_length=32,
    )
    active = models.BooleanField(default=True)

    param = models.CharField(
        max_length=32,
    )

    class Meta:
        ordering = ['name']


class DeliveryPricing(models.Model):
    """
    Courier/post price list

    """

    objects = DeliveryPriceManager()

    delivery_option = models.ForeignKey(
        DeliveryOption,
        on_delete=models.DO_NOTHING,
    )

    max_param = models.FloatField()
    price = CashField()

    class Meta:
        ordering = ['delivery_option', 'max_param']
        unique_together = (
            ('delivery_option', 'max_param')
        )

    def __str__(self):
        return '{} {}'.format(
            self.delivery_option.name,
            self.price,
        )

class Delivery(models.Model):
    """
    Delivery price and option
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
    )
    delivery_option = models.ForeignKey(
        DeliveryOption,
        on_delete=models.SET(value='0'),
    )
    value = CashField()
