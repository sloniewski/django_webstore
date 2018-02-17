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

    @property
    def max_param(self):
        return self.deliverypricing_set.last().max_param


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

    def form_choice(self, delimiter='-'):
        text = '{}{}{}'.format(
            self.delivery_option.name,
            delimiter,
            str(self.price),
        )
        return text, text

    @property
    def param(self):
        return self.delivery_option.param

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
