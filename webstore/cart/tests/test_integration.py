from importlib import import_module
from http.cookies import SimpleCookie

from django.test import TestCase
from django.shortcuts import reverse
from django.conf import settings
from django.http import JsonResponse

from webstore.cart.models import Cart, CartItem
from webstore.product.models import Product, Price
from webstore.core.utils import random_string


class TestIntegration(TestCase):

    def setUp(self):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        self.session = SessionStore()
        self.session.create()
        self.session.save()

        self.cart = Cart.objects.get_or_create(session=self.session)[0]
        self.client.cookies = SimpleCookie({'sessionid': self.session.session_key})

    def create_test_product(self, name=None, price=None):
        '''
        Helper method for creating Product objects
        '''

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

    def test_cart_item_list_view(self):
        item = self.create_test_product(price='78')
        self.cart.add_item(item=item.id, qty=5)
        response = self.client.get(
            path=reverse('cart:item-list'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='webstore/cart/cart_list.html',
        )
        self.assertContains(response, item.name)

    def test_cart_item_delete(self):
        product = self.create_test_product(price='78')
        self.cart.add_item(item=product.id, qty=5)
        response = self.client.post(
            reverse(
                'cart:quick-delete-item',
                kwargs={'item_id': product.id}
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(product=product, cart=self.cart, quantity=5)
