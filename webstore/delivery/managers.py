from django.db import models


class DeliveryManager(models.Manager):
    pass


class DeliveryPriceManager(models.Manager):

    def get_prices_for_cart(self, cart):
        prices = self.get_queryset().all()
        weight = cart.weight
        return [
            (str(x.cost_per_kg*weight).split(' ')[0],
             x.name + ': ' + str(x.cost_per_kg*weight))
            for x in prices
        ]
