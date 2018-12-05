from django.db import models


class DeliveryQuerySet(models.QuerySet):

    def get_last(self, user):
        return self.filter(order__user=user).order_by('-created').first()


class DeliveryManager(models.Manager):

    def get_queryset(self):
        return DeliveryQuerySet(self.model, using=self.db)

    def get_last(self, user):
        return self.get_queryset().get_last(user)


class DeliveryPriceManager(models.Manager):

    def get_prices_for_cart(self, cart):
        prices = self.get_queryset().all()
        print(cart.weight)
        return [
            (x.get_price(cart.weight), x.name+': '+str(x.get_price(cart.weight)))
            for x in prices
        ]
