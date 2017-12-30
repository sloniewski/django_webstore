from django.shortcuts import reverse
from django.test import TestCase

from . import Product


class TestProductView(TestCase):

    def get_response(self):
        product = Product.objects.create(
            name='The Holy Grail',
        )
        response = self.client.get(
            reverse('product:product-detail', kwargs={'slug': product.slug}))
        return response

    def test_http_status(self):
        self.assertEqual(
            first=self.get_response().status_code,
            second=200,
            msg='view did not return expected response',
        )

    def test_template_used(self):
        self.assertTemplateUsed(
            self.get_response(),
            'product/product-detail.html',
        )


