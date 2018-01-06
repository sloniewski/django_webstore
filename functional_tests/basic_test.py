from product.models import Product

from .base import FunctionalTest


class BasicTest(FunctionalTest):

    def test_if_functional_tests_work(self):
        product = Product.objects.create(name='my-test-product')
        self.browser.get('http://localhost:8000/product/{}/'.format(product.slug))
        self.assertIn('my test product', self.browser.title)


