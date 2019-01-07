from django.shortcuts import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from webstore.order.views import OrderListView
from webstore.order.models import Order
from webstore.delivery.models import Delivery


User = get_user_model()


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='username', password='123')
        self.client.login(username='username', password='123')
        self.order = Order.objects.create(user=self.user)
        self.request_factory = RequestFactory()

        self.delivery_data = {
            'name': 'xxx',
            'surname': 'yyy',
            'city': 'neverland',
            'country': 'trinidad tobago',
            'postal_code': '00000',
            'street_name': 'test delivery',
            'street_number': 1,
            'flat_number': 4,
            'cost': '22.22',
            'order': self.order,
        }
        self.delivery = Delivery.objects.create(**self.delivery_data)

    def test_list_view_queryset(self):
        request = self.request_factory.get(
            reverse('order:order-list')
        )
        request.user = self.user
        view = OrderListView()
        view.request = request
        self.assertEqual(list(view.get_queryset()), [self.order])
