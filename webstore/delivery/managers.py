from django.db import models


class DeliveryManager(models.Manager):
    pass


class DeliveryPriceManager(models.Manager):

    def get_prices_for_cart(self, cart):
        prices = self.get_queryset().all()
        print(cart.weight)
        return [
            (x.get_price(cart.weight), x.name+': '+str(x.get_price(cart.weight)))
            for x in prices
        ]
