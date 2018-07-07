from django.db import models


class DeliveryManager(models.Manager):
    pass


class DeliveryPriceManager(models.Manager):

    def get_prices_for_cart(self, cart):
        return [(x, x+2) for x in range(5)]
