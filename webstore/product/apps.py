from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = 'webstore.product'

    def ready(self):
        from . import handlers
