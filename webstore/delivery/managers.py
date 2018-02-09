import inspect

from django.db import models

from webstore.delivery import models as deliver_models


class DeliveryManager(object):
    """
    Provides interface for interacting with delivery module
    """
    _couriers = []
    
    def __init__(self):
        _couriers = self._get_delivery_options()

    def get_form_choices(self, order):
        choices = []
        for courier in _couriers:
            choices.append(
                (courier.name, courier.objects.get_price_for_order(order_weight=order.weight, order_cbm=order.cbm))
            )
        return choices
            

    def _get_delivery_options(self):
        for name, klass in inspect.getmembers(deliver_models):
            try:
                if issubclass(klass, (deliver_models.DeliveryOption,)):
                    self._couriers.append(klass)
            except TypeError:
                continue

class AbstractDeliveryManager(models.Manager):
    """
    Each new delivery option (courier pricing) manager should implement this class
    """
    default_evaluation_method = None
    
    def get_price_for_order(self, order_weight=None, order_cbm=None):
        if default_evaluation_method is None:
            raise AttributeError('No evaluation set for this delivery option, set \'default_evaluation_method\', on manager')
        else:
            try:
                evaluation_method = getattr(self, self.default_evaluation_method)
            except AttributeError:
                raise AttributeError('{} method is missing, make sure to add it on delivery manager'.format(self.default_evaluation_method))
            param = order_weight or order_cbm
            return evaluation_method(param)
    
    def get_cbm_price(self, weight):
        raise NotImplementedError('Volume pricing not impemented for this delivery option')
        
    def get_weight_price(self, cbm):
        raise NotImplementedError('Weight pricing not impemented for this delivery option')