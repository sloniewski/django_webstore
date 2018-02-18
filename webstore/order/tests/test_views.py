from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from webstore.order.models import Order
from webstore.order import views


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


class TestAddDeliveryView(TestCase):
    
    def setUp(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(user=user)
        self.response = self.client.get(
            reverse('order:order-confirm', kwargs={'pk': order.id})
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
            template_name='order/order_add_delivery.html',
        )

    def test_view_function(self):
        self.assertEqual(views.OrderAddDeliveryView.as_view().__name__, self.response.resolver_match.func.__name__)


class TestOrderListView(TestCase):
    
    def setUp(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(user=user)
        self.response = self.client.get(
            reverse('order:order-list', kwargs={})
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
            template_name='order/order_list.html',
        )

    def test_view_function(self):
        self.assertEqual(views.OrderListView.as_view().__name__, self.response.resolver_match.func.__name__)


class TestAddPaymentViw(TestCase):

    def setUp(self):
        user = User.objects.create(username='test_user')
        order = Order.objects.create(user=user)
        self.response = self.client.get(
            reverse('order:order-payment', kwargs={'pk': order.id})
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
            template_name='order/order_add_payment.html',
        )

    def test_view_function(self):
        self.assertEqual(views.OrderAddPaymentView.as_view().__name__, self.response.resolver_match.func.__name__)