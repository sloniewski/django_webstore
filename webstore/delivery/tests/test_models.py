from unittest.mock import Mock

from django.test import TestCase

from webstore.delivery.models import DeliveryPricing


class TestDeliveryPricingModel(TestCase):

    def setUp(self):
        DeliveryPricing.objects.bulk_create([
            DeliveryPricing(name='test1', cost_per_kg=1.1),
            DeliveryPricing(name='test2', cost_per_kg=2.2),
            DeliveryPricing(name='test3', cost_per_kg=3.3),
        ])

    def test_prices_for_cart(self):
        cart = Mock()
        cart.weight = 1
        prices = DeliveryPricing.objects.get_prices_for_cart(cart)
        self.assertEqual(
            [('1.1', '1.1'), ('2.2', '2.2'), ('3.3', '3.3')],
            prices
        )
