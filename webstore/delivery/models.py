from django.db import models

from webstore.cash.fields import CashField
from webstore.delivery.managers import (
    AbstractDeliveryManager,
    SomeCourierManager,
    AnotherCourierManager,
)


class AbstractDeliveryOption(models.Model):
    """
    Each new delivery option (courier pricing) should inherit from this class
    """

    name = None
    objects = AbstractDeliveryManager()

    class Meta:
        abstract = True

    def __str__(self):
        if self.name is None:
            raise NotImplementedError('No name set for delivery option')
        return '{} - {}'.format(
            self.name,
            self.price,
        )


class SomeCourierPricing(AbstractDeliveryOption):
    """
    Example of weight based courier price list
    """
    name = 'Some Courier'
    objects = SomeCourierManager()

    max_weight = models.FloatField(unique=True)
    price = CashField()

    class Meta:
        ordering = ['max_weight']


class AnotherCourierPricing(AbstractDeliveryOption):
    """
    Example of volume base price list
    """
    name = 'Another Courier'
    objects = AnotherCourierManager()

    max_cbm = models.FloatField()
    price = CashField()

    class Meta:
        ordering = ['max_cbm']
