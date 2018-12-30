from datetime import date
from urllib.parse import urlencode
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from webstore.order.models import Order, OrderItem, OrderStatus
from webstore.product.models import (
    Product,
    Category,
    Price,
)

User = get_user_model()


class TestViews(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='for delete')
        self.product = Product.objects.create(name='The Holy Grail')
        self.product_2 = Product.objects.create(name='shrubbery')
        self.product.categories.add(self.category)
        self.price = Price.objects.create(
            value='11.11',
            valid_from=date(year=2017, month=1, day=1),
            product=self.product,
        )
        self.price_2 = Price.objects.create(
            value='12.12',
            valid_from=date(year=2017, month=1, day=1),
            product=self.product_2,
        )
        self.user = User.objects.create(username='username')
        self.order = Order.objects.create(
            user=self.user
        )
        self.delete_order = Order.objects.create(
            user=self.user
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=36,
            price=self.price.value,
        )
        self.delete_order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product_2,
            quantity=1,
            price=self.price.value,
        )

    def test_order_list_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-list',
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order/order_list.html')

    def test_order_detail_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-detail',
                kwargs={'uuid': self.order.uuid},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order/order_detail.html')
        self.assertContains(response, self.order_item.product.name)

    def test_order_delete_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-delete',
                kwargs={'uuid': self.delete_order.uuid},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/generic_delete.html')

    def test_order_delete_post(self):
        temp_id = self.delete_order.id
        response = self.client.post(
            reverse(
                viewname='order_panel:order-delete',
                kwargs={'uuid': self.delete_order.uuid},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('order_panel:order-list'))
        with self.assertRaises(Order.DoesNotExist):
            ord = Order.objects.get(id=temp_id)

    def test_order_update_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-update',
                kwargs={'uuid': self.order.uuid},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order/order_update.html')

    def test_order_update_post(self):
        data = {
            'status': OrderStatus.SHIPPING.name,
        }
        response = self.client.post(
            reverse(
                viewname='order_panel:order-update',
                kwargs={'uuid': self.order.uuid},
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('order_panel:order-list'))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, OrderStatus.SHIPPING.name)

    def test_order_edit_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-edit',
                kwargs={'uuid': self.order.uuid},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order/order_item_edit.html')

    def test_order_item_update_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-item-update',
                kwargs={'pk': self.order_item.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order/order_item_update.html')

    def test_order_item_update_post(self):
        data = {
            'quantity': 8,
            'price': 5,
        }
        response = self.client.post(
            reverse(
                viewname='order_panel:order-item-update',
                kwargs={'pk': self.order_item.id},
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('order_panel:order-detail', kwargs={'uuid': self.order.uuid}))
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, data['quantity'])
        self.assertEqual(self.order_item.price, Decimal(data['price']))

    def test_order_item_update_delete_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-item-delete',
                kwargs={'pk': self.delete_order_item.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order/order_item_delete.html')

    def test_order_item_update_delete_post(self):
        temp_id = self.delete_order_item.id
        response = self.client.post(
            reverse(
                viewname='order_panel:order-item-delete',
                kwargs={'pk': self.delete_order_item.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response, reverse('order_panel:order-detail', kwargs={'uuid': self.order.id}))
        with self.assertRaises(OrderItem.DoesNotExist):
            item = OrderItem.objects.get(id=temp_id)
