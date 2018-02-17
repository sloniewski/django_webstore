from django.db import models


class DeliveryManager(models.Manager):

    pass


class DeliveryPriceQueryset(models.QuerySet):

    def price_sets(self):
        for option in self.values('delivery_option').distinct().order_by('delivery_option'):
            yield self.filter(delivery_option__id=option['delivery_option'])


class DeliveryPriceManager(models.Manager):

    def get_queryset(self):
        return DeliveryPriceQueryset(self.model, using=self._db)

    def get_prices_for_order(self, order):
        result = []
        for price_set in self.get_queryset().price_sets():
            param = price_set[0].delivery_option.param
            param_value = getattr(order, param)
            for tariff in price_set:
                if tariff.max_param > param_value:
                    result.append(tariff)
                    break
        return result
