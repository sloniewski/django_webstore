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
    cost = CashField()

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return 'Delivery no. {} cost: {}'.format(self.pk, self.cost)

    def __repr__(self):
        return self.__str__()


class DeliveryPricing(models.Model):
    objects = DeliveryPriceManager()

    name = models.CharField(max_length=64)
    cost_per_kg = CashField()

    def __str__(self):
        return 'Name: {}, price: {}'.format(self.name, self.cost_per_kg)

    def __repr__(self):
        return self.__str__()
