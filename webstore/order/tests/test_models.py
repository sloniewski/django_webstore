from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from webstore.product.models import Product, Price
from webstore.core.utils import random_string
from webstore.order.models import Order, OrderItem


User = get_user_model()

def create_test_product(name=None, price='45.76'):
    if name is None:
        name = 'product' + random_string(6)
    product = Product.objects.create(name=name)

    if price is None:
        return product

    Price.objects.create(
        value=price,
        valid_from='2018-01-01',
        product=product,
    )
    return product


class TestOrderModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_user")

    def test_order_value(self):
        order = Order.objects.create(
            user=self.user,
        )
        product_1 = create_test_product(name='test_product_1')
        product_2 = create_test_product(name='test_product_1')
        order_item_1 = OrderItem.objects.create(
            order=order,
            product=product_1,
            quantity=4,
            price='11.11',
        )
        order_item_2 = OrderItem.objects.create(
            order=order,
            product=product_2,
            quantity=2,
            price='22.22',
        )
        self.assertEquals(order.value, Decimal('88.88'))
        self.assertIsInstance(order.value, Decimal)

    def test_order_has_uuid_assigned(self):
        orders = [Order(user=self.user) for _ in range(100)]
        for o in orders:
            o.save()
            o.refresh_from_db()
        ids = [ord.uuid for ord in orders]
        self.assertEqual(len(orders), len(set(ids)))


class TestOrderItemModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.order = Order.objects.create(user=self.user)

    def test_order_item_value(self):
        product = create_test_product(name='test_product')
        order_item = OrderItem.objects.create(
            order=self.order,
            product=product,
            quantity=2,
            price='11.11',
        )
        order_item.refresh_from_db()
        self.assertIsInstance(order_item.price, Decimal)
        self.assertEqual(order_item.value, Decimal('22.22'))
        self.assertIsInstance(order_item.value, Decimal)
