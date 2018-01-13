from django.shortcuts import reverse
from django.test import TestCase

from webstore.product.models import Product


class TestProductView(TestCase):

    def setUp(self):
        product = Product.objects.create(
            name='The Holy Grail',
        )
        self.response = self.client.get(
            reverse('product:product-detail', kwargs={'slug': product.slug})
        )

    def test_http_status(self):
        self.assertEqual(
            first=self.response.status_code,
            second=200,
            msg='view did not return expected response',
        )

    def test_template_used(self):
        self.assertTemplateUsed(
            response=self.response,
            template_name='product/product_detail.html',
        )


