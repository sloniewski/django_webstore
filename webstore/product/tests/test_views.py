from django.test import TestCase

from webstore.product.models import Product, Price
from webstore.product.views import ProductDetailView


class TestDetailView(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='The Holy Grail',
        )
        self.price = Price(
            value=12.0101,
            valid_from='2018-01-01',
            product=self.product,
        )

    def test_queryset(self):
        view = ProductDetailView()
        qs = view.get_queryset()
        self.assertIn(self.product, qs)
