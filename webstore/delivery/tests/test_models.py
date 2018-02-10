from django.test import TestCase

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
        price = SomeCourierPricing.objects.get_price_for_order(order_weight=7.2, order_cbm=0.5)
        self.assertEqual(price, Cash('18.51'))
        self.assertIsInstance(price, Cash)

    def test_pricing_manager_with_larger_weight(self):
        price = SomeCourierPricing.objects.get_price_for_order(order_weight=20.2)
        self.assertEqual(price, Cash('24.88'))
        self.assertIsInstance(price, Cash)


class TestAnotherCourierPricing(TestCase):

    def setUp(self):
        AnotherCourierPricing.objects.bulk_create([
            AnotherCourierPricing(max_cbm=1.5, price='18.51'),
            AnotherCourierPricing(max_cbm=2.2, price='24.88'),
            AnotherCourierPricing(max_cbm=0.5, price='12.02'),
        ])

    def test_pricing_manager(self):
        price = AnotherCourierPricing.objects.get_price_for_order(order_cbm=1.1)
        self.assertEqual(price, Cash('18.51'))
        self.assertIsInstance(price, Cash)


