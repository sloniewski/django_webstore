from django.test import TestCase
from django.shortcuts import reverse

from webstore.delivery.models import DeliveryPricing


class TestDeliveryViews(TestCase):
    def setUp(self):
        self.delivery_option = DeliveryPricing.objects.create(
            name='test',
            cost=32.99,
        )

    def test_delivery_list(self):
        response = self.client.get(
            reverse(viewname='delivery_panel:delivery-list')
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/delivery/delivery_list.html',
        )

    def test_delivery_price_list(self):
        response = self.client.get(
            reverse(viewname='delivery_panel:delivery-option-list')
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/delivery/delivery_option_list.html',
        )

    def test_delivery_price_update(self):
        response = self.client.get(
            reverse(
                viewname='delivery_panel:delivery-option-update',
                kwargs={'pk': self.delivery_option.pk},
            )
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/delivery/delivery_option_update.html',
        )
