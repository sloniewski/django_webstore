import inspect

from django.db import models

from webstore.delivery import models as deliver_models
from webstore.cash.models import Cash


class DeliveryManager(object):
    """
    Provides interface for interacting with delivery module
    """
    _couriers = []
    
    def __init__(self):
        self._couriers = self._get_delivery_options()

    def get_form_choices(self, order):
        choices = []
        for courier in self._couriers:
            choices.append(
                (courier.name, courier.objects.get_price_for_order(order_weight=order.weight, order_cbm=order.cbm))
            )
        return choices
            
    def _get_delivery_options(self):
        result = []
        for name, klass in inspect.getmembers(deliver_models):
            try:
                if issubclass(klass, (deliver_models.AbstractDeliveryOption,)):
                    result.append(klass)
            except TypeError:
                continue
        return result


class AbstractDeliveryManager(models.Manager):
    """
    Each new delivery option (courier pricing) manager should implement this class
    """
    default_evaluation_method = None

    def get_price_for_order(self, order_weight=None, order_cbm=None):
        if self.default_evaluation_method is None:
            raise AttributeError('No evaluation set for this delivery option, set \'default_evaluation_method\', on manager')
        else:
            try:
                evaluation_method = getattr(self, self.default_evaluation_method)
            except AttributeError:
                raise AttributeError('{} method is missing, make sure to add it on delivery manager'.format(self.default_evaluation_method))
            param = order_weight or order_cbm
            return evaluation_method(param)
    

class SomeCourierManager(AbstractDeliveryManager):
    """
    Example of manager that gets price by weight
    """

    default_evaluation_method = 'get_price_for_weight'

    def get_price_for_weight(self, weight):
        for tariff in self.get_queryset().all():
            if tariff.max_weight > weight:
                return tariff.price
        return None

    def _split_weight(self, weight):
        max_val = self._get_max_weight()
        result = []
        if weight <= max_val:
            result.append(weight)
        else:
            whole_values = weight // max_val
            for x in range(whole_values):
                result.append(max_val)
            rest = weight % max_val
            result.append(rest)
        return result


    def _get_max_weight(self):
        last_tariff = self.get_queryset().last()
        return last_tariff.max_weight


class AnotherCourierManager(AbstractDeliveryManager):
    """
    Example of manager that gets price by volume
    """

    default_evaluation_method = 'get_price_for_cbm'

    def get_price_for_cbm(self, cbm):
        for tariff in self.get_queryset().all():
            if tariff.max_cbm > cbm:
                return tariff.price
        return None