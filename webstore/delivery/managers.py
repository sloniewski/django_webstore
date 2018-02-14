import inspect

from django.db import models

from webstore.delivery import models as deliver_models


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
    default_evaluation_method = 'get_price'
    param = None

    def get_price_for_order(self, order):
        if self.default_evaluation_method is None:
            raise AttributeError('No evaluation set for this delivery option, set \'default_evaluation_method\', on manager')
        else:
            try:
                evaluation_method = getattr(self, self.default_evaluation_method)
            except AttributeError:
                raise AttributeError('{} method is missing, make sure to add it on delivery manager'.format(self.default_evaluation_method))
            param = self.get_param(order)
            return evaluation_method(param)

    def get_param(self, order):
        param = getattr(order, self.param)
        return param


class SomeCourierManager(AbstractDeliveryManager):
    """
    Example of manager that gets price by weight
    """
    param = 'weight'

    def get_price(self, weight):
        for tariff in self.get_queryset().all():
            if tariff.max_weight > weight:
                return tariff.price
        return None


class AnotherCourierManager(AbstractDeliveryManager):
    """
    Example of manager that gets price by volume
    """
    param = 'cbm'

    def get_price(self, cbm):
        for tariff in self.get_queryset().all():
            if tariff.max_cbm > cbm:
                return tariff.price
        return None