from django.db import models


class DeliveryOption(models.Model):
    """
    Each new delivery option should inherit from this class
    """

    name = None

    def get_price(self, order_weight=None, order_cbm=None):
        raise NotImplementedError

    class Meta:
        abstract = True

    def __str__(self):
        if self.name is None:
            raise NotImplementedError('No name set for delivery option')
        return self.name


class SomeCourierPricing(DeliveryOption):
    name = 'Some Courier'

    def get_price(self, order_weight=None, order_cbm=None):
        pass


class AnotherCourier(DeliveryOption):
    name = 'Another Courier'

    def get_price(self, order_weight=None, order_cbm=None):
        pass
