import inspect

from webstore.delivery import models as deliver_models

class DeliveryManager(object):
    """
    Provides interface for interacting with delivery module
    """
    _couriers = []

    @staticmethod
    def get_form_choices(self, order):
        pass

    def _get_delivery_options(self):
        for name, klass in inspect.getmembers(deliver_models):
            try:
                if issubclass(klass, (deliver_models.DeliveryOption,)):
                    self._couriers.append()
            except TypeError:
                continue

