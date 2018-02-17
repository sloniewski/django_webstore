from unittest import skip

from django.test import TestCase

from webstore.order.models import Order
from webstore.delivery.models import DeliveryOption, DeliveryPricing
from webstore.cash.models import Cash


class TestDeliveryPricingModel(TestCase):

    def setUp(self):
        option = DeliveryOption.objects.create(
            name='test',
            param='weight'
        )
        DeliveryPricing.objects.bulk_create([
            DeliveryPricing(max_param=10.8, price='18.51', delivery_option=option),
            DeliveryPricing(max_param=15.1, price='24.88', delivery_option=option),
            DeliveryPricing(max_param=5.5, price='12.02', delivery_option=option),
        ])

    def test_pricing_manager(self):
        order = Order()
        order.weight = 7.2
        price = DeliveryPricing.objects.get_prices_for_order(order)
        self.assertEqual(price[0].price, Cash('18.51'))
        self.assertIsInstance(price[0].price, Cash)

        order.weight = 3.2
        price = DeliveryPricing.objects.get_prices_for_order(order)
        self.assertEqual(price[0].price, Cash('12.02'))
        self.assertIsInstance(price[0].price, Cash)

        order.weight = 13.2
        price = DeliveryPricing.objects.get_prices_for_order(order)
        self.assertEqual(price[0].price, Cash('24.88'))
        self.assertIsInstance(price[0].price, Cash)

    @skip
    def test_pricing_manager_with_larger_weight(self):
        order = Order()
        order.weight = 18.2
        price = DeliveryOption.objects.get_price_for_order(order)
        self.assertEqual(price.price, Cash('36.9'))
        self.assertIsInstance(price.price, Cash)

