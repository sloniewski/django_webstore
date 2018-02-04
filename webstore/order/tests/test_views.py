from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from webstore.order.models import Order


User = get_user_model()

class TestOrderView(TestCase):

    def setUp(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(user=user)
        self.response = self.client.get(
            reverse('order:order-detail', kwargs={'pk': order.id})
        )

    def test_http_status(self):
        self.assertEqual(
            first=self.response.status_code,
            second=200,
            msg='view returned {} code'.format(self.response.status_code),
        )

    def test_template_used(self):
        self.assertTemplateUsed(
            response=self.response,
            template_name='order/order_detail.html',
        )
