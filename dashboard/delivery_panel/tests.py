from urllib.parse import urlencode
from decimal import Decimal

from django.test import TestCase
from django.shortcuts import reverse

from webstore.delivery.models import DeliveryPricing


class TestDeliveryViews(TestCase):
    """ Tests for authenticated user """

    def setUp(self):
        self.delivery_option = DeliveryPricing.objects.create(
            name='test',
            cost=32.99,
        )
        self.delete_this = DeliveryPricing.objects.create(
            name='delete_this',
            cost=12.49,
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

    def test_delivery_price_update_get(self):
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

    def test_delivery_price_update_post(self):
        data = {
            'name': 'changed_name',
            'cost': 99.99,
            'active': 'on',
            'max_weight': 25,
        }
        response = self.client.post(
            reverse(
                viewname='delivery_panel:delivery-option-update',
                kwargs={'pk': self.delivery_option.pk},
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(
            first=response.status_code,
            second=302,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertEqual(
            first=response.url,
            second=reverse('delivery_panel:delivery-option-list')
        )

        self.delivery_option.refresh_from_db()
        self.assertEqual(self.delivery_option.name, 'changed_name')
        self.assertEqual(self.delivery_option.max_weight, 25)
        self.assertEqual(self.delivery_option.active, True)
        self.assertEqual(self.delivery_option.cost, Decimal('99.99'))

    def test_delivery_price_delete_get(self):
        response = self.client.get(
            reverse(
                viewname='delivery_panel:delivery-option-delete',
                kwargs={'pk': self.delivery_option.pk},
            )
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
            msg='view returned {} code'.format(response.status_code),
        )

    def test_delivery_price_delete_post(self):
        deleted_item_pk = self.delete_this.id
        response = self.client.post(
            reverse(
                viewname='delivery_panel:delivery-option-delete',
                kwargs={'pk': self.delete_this.pk},
            )
        )
        self.assertEqual(
            first=response.status_code,
            second=302,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertEqual(
            first=response.url,
            second=reverse('delivery_panel:delivery-option-list'),
        )
        with self.assertRaises(DeliveryPricing.DoesNotExist):
            not_existing = DeliveryPricing.objects.get(pk=deleted_item_pk)

    def test_delivery_price_create_get(self):
        response = self.client.get(
            reverse(
                viewname='delivery_panel:delivery-option-create',
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

    def test_delivery_price_create_post(self):
        data = {
            'name': 'test_name',
            'cost': 11.37,
            'active': 'on',
            'max_weight': 20,
        }
        response = self.client.post(
            reverse(
                viewname='delivery_panel:delivery-option-create',
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(
            first=response.status_code,
            second=302,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertEqual(
            first=response.url,
            second=reverse('delivery_panel:delivery-option-list')
        )

        delivery_option = DeliveryPricing.objects.get(
            name='test_name',
            max_weight=20,
            active=True,
        )
        self.assertEqual(delivery_option.name, 'test_name')
        self.assertEqual(delivery_option.max_weight, 20)
        self.assertEqual(delivery_option.active, True)
        self.assertEqual(delivery_option.cost, Decimal('11.37'))



