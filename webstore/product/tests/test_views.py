from django.shortcuts import reverse
from django.test import TestCase

from webstore.product.models import Product, Price


class TestProductViews(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='The Holy Grail',
        )
        self.price = Price(
            value=12.0101,
            valid_from='2018-01-01',
            product=self.product,
        )

    def test_product_list_get(self):
        response = self.client.get(
            reverse('product:product-list')
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
        )
        self.assertTemplateUsed(
            response=response,
            template_name='webstore/product/product_list.html',
        )

    def test_product_detail(self):
        response = self.client.get(
            reverse('product:product-detail', kwargs={'slug':self.product.slug})
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
        )
        self.assertTemplateUsed(
            response=response,
            template_name='webstore/product/product_detail.html',
        )



