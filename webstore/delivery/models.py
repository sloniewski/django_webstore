from django.db import models

from webstore.delivery.managers import AbstractDeliveryManager


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
        return self.name


class SomeCourierPricing(AbstractDeliveryOption):
    name = 'Some Courier'



class AnotherCourier(AbstractDeliveryOption):
    name = 'Another Courier'

    