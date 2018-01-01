from selenium import webdriver
from django.test import TestCase
from product.models import Product


class BasicTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_if_functional_tests_work(self):
        product = Product.objects.create(name='my-test-product')
        self.browser.get('http://localhost:8000/product/{}/'.format(product.slug))
        self.assertIn('my test product', self.browser.title)


