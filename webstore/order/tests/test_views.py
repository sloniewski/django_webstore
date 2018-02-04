from django.shortcuts import reverse
from django.test import TestCase

from .models import Order

class TestOrderView(TestCase):

    def setUp(self):
        product = Order.objects.create()
        self.response = self.client.get(
            reverse('order:order-detail', kwargs={'slug': product.slug})
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
            template_name='order/order_detail.html',
        )
