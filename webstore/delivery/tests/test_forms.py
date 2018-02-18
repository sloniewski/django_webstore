from django.test import TestCase

from webstore.order.models import Order
from webstore.delivery.models import DeliveryOption, DeliveryPricing
from webstore.delivery.forms import ChooseDeliveryForm


class TestChooseDeliveryForm(TestCase):

    def setUp(self):
        option = DeliveryOption.objects.create(
            name='test',
            param='test'
        )
        DeliveryPricing.objects.bulk_create([
            DeliveryPricing(max_param=10.8, price='18.51', delivery_option=option),
            DeliveryPricing(max_param=15.1, price='24.88', delivery_option=option),
            DeliveryPricing(max_param=5.5, price='12.02', delivery_option=option),
        ])

    def test_basics(self):

        order = Order()
        order.test = 12.2
        form = ChooseDeliveryForm(order=order)

        self.assertEqual(1, len(form.fields))
        self.assertEqual(1, len(form.fields['option'].choices))
