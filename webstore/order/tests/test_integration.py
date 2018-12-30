from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from webstore.order.models import Order


User = get_user_model()


class TestIntegration(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='123')
        self.client.login(username='test_user', password='123')
        self.order = Order.objects.create(user=self.user)

    def test_order_detail(self):
        response = self.client.get(
            reverse('order:order-detail', kwargs={'uuid': self.order.uuid})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webstore/order/order_detail.html')

    def test_order_confirm_get(self):
        response = self.client.get(reverse('order:order-confirm'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'webstore/order/order_add_delivery.html')

    def test_order_list_view_get(self):
        response = self.client.get(reverse('order:order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webstore/order/order_list.html')

    def test_order_summary_get(self):
        response = self.client.get(
            reverse('order:order-summary', kwargs={'uuid': self.order.uuid})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webstore/order/order_summary.html')
