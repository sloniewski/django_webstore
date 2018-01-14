from importlib import import_module

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from webstore.product.models import Product, Price
from webstore.product.utils import random_string

from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        self.session = SessionStore()

    def tearDown(self):
        self.browser.quit()

    def create_test_product(self, name=None, price=None):
        if name is None:
            name = random_string(6)
        product = Product.objects.create(name=name)

        if price is None:
            return product

        Price.objects.create(
            value=price,
            valid_from='2018-01-01',
            product=product,
        )
        return product


