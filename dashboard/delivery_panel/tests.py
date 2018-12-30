from urllib.parse import urlencode
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse

from webstore.delivery.models import DeliveryPricing, Delivery
from webstore.order.models import Order

User = get_user_model()


class TestsIntegrated(TestCase):
    """ Tests for authenticated user """

    def setUp(self):
        self.user = User.objects.create(username='username')
        self.order = Order.objects.create(user=self.user)
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
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'dashboard/delivery/delivery_list.html')
        self.assertContains(response, self.order.uuid)

    def test_delivery_update_get(self):
        response = self.client.get(
            reverse(
                'delivery_panel:delivery-update',
                kwargs={'pk': self.delivery.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/delivery/delivery_update.html')

    def test_delivery_update_post(self):
        self.delivery_data['street_number'] = 55
        response = self.client.post(
            reverse(
                'delivery_panel:delivery-update',
                kwargs={'pk': self.delivery.id},
            ),
            data=self.delivery_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('delivery_panel:delivery-list'))
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.street_number, '55')

    def test_delivery_detail_get(self):
        response = self.client.get(
            reverse(
                'delivery_panel:delivery-detail',
                kwargs={'pk': self.delivery.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/delivery/delivery_detail.html')

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



