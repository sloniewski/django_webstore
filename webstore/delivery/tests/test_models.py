from django.test import TestCase

from webstore.order.models import Order
from webstore.delivery.models import SomeCourierPricing, AnotherCourierPricing
from webstore.cash.models import Cash


class TestSomeCourierPricingModel(TestCase):

    def setUp(self):
        SomeCourierPricing.objects.bulk_create([
            SomeCourierPricing(max_weight=10.8, price='18.51'),
            SomeCourierPricing(max_weight=15.1, price='24.88'),
            SomeCourierPricing(max_weight=5.5, price='12.02'),
        ])

    def test_pricing_manager(self):
        order = Order()
        order.weight = 7.2
        price = SomeCourierPricing.objects.get_price_for_order(order)
        self.assertEqual(price.price, Cash('18.51'))
        self.assertIsInstance(price.price, Cash)

    def test_pricing_manager_with_larger_weight(self):
        order = Order()
        order.weight = 18.2
        price = SomeCourierPricing.objects.get_price_for_order(order)
        self.assertEqual(price.price, Cash('36.9'))
        self.assertIsInstance(price.price, Cash)


class TestAnotherCourierPricing(TestCase):

    def setUp(self):
        AnotherCourierPricing.objects.bulk_create([
            AnotherCourierPricing(max_cbm=1.5, price='18.51'),
            AnotherCourierPricing(max_cbm=2.2, price='24.88'),
            AnotherCourierPricing(max_cbm=0.5, price='12.02'),
        ])

    def test_pricing_manager(self):
        order = Order()
        order.cbm = 1.1
        price = AnotherCourierPricing.objects.get_price_for_order(order)
        self.assertEqual(price.price, Cash('18.51'))
        self.assertIsInstance(price.price, Cash)

    def test_pricing_manager_with_larger_cbm(self):
        order = Order()
        order.cbm = 2.5
        price = AnotherCourierPricing.objects.get_price_for_order(order)
        self.assertEqual(price.price, Cash('36.9'))
        self.assertIsInstance(price.price, Cash)


