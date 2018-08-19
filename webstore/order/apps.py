from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'webstore.order'

    def ready(self):
        from . import handlers
