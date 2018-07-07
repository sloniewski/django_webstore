from django.db import models

from webstore.order.models import Order
from webstore.cash.fields import CashField
from webstore.delivery.managers import (
    DeliveryPriceManager,
    DeliveryManager,
)


class Delivery(models.Model):
    objects = DeliveryManager()

    name = models.CharField(max_length=64, null=True)
    surname = models.CharField(max_length=64, null=True)
    street_name = models.CharField(max_length=64)
    street_number = models.CharField(max_length=16)
    flat_number = models.CharField(max_length=16, null=True)
    price = CashField()

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
    )


class DeliveryPricing(models.Model):
    objects = DeliveryPriceManager()

    name = models.CharField(max_length=64)
    cost_per_kg = CashField()
