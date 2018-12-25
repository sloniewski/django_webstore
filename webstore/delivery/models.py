from math import ceil

from django.db import models

from webstore.order.models import Order
from webstore.core.mixins import TimeStampMixin
from webstore.delivery.managers import (
    DeliveryPriceManager,
    DeliveryManager,
)


class Delivery(TimeStampMixin, models.Model):
    objects = DeliveryManager()
    iterable_attrs = [
        'name', 'surname', 'street_name', 'street_number',
        'flat_number', 'postal_code', 'city', 'country',
    ]

    name = models.CharField(max_length=64, null=True)
    surname = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=64, null=True)
    country = models.CharField(max_length=64, null=True)
    postal_code = models.CharField(max_length=16, null=True)
    street_name = models.CharField(max_length=64)
    street_number = models.CharField(max_length=16)
    flat_number = models.CharField(max_length=16, null=True)
    cost = models.DecimalField(
        decimal_places=2,
        max_digits=8,
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery',
    )

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return 'Delivery no. {} cost: {}'.format(self.pk, self.cost)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.iterable_attrs):
            attr_name = self.iterable_attrs[self.n]
            attr_val = getattr(self, attr_name)
            result = (attr_name, attr_val)
            self.n += 1
            return result
        else:
            raise StopIteration

    @property
    def status(self):
        return self.order.status


class DeliveryPricing(models.Model):
    objects = DeliveryPriceManager()

    name = models.CharField(max_length=64)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    max_weight = models.FloatField(default=30.00)

    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Name: {}, price: {}'.format(self.name, self.cost)

    def __repr__(self):
        return self.__str__()

    def get_price(self, weight):
        parcels_num = weight / self.max_weight
        return self.cost * ceil(parcels_num)
