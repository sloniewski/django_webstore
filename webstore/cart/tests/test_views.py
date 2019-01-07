from http.cookies import SimpleCookie
from importlib import import_module

from django.shortcuts import reverse
from django.test import TestCase
from django.conf import settings

from webstore.product.models import Product
from webstore.cart.models import Cart

import json


class TestAddItemView(TestCase):
    '''
    Tests view responsible for adding items to cart
    ''' 

    def setUp(self):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        self.session = SessionStore()
        self.session.create()
        self.session.save()

        self.cart = Cart.objects.create(session=self.session)

        self.product = Product.objects.create(name='Mint Chocolate')

    def test_get_raises_404(self):
        response = self.client.get(
            reverse('cart:add-item'),
        )
        self.assertEqual(response.status_code, 404)

    def test_on_post_return_400_when_params_missing(self):
        response = self.client.post(
            path=reverse('cart:add-item'),
            data={
                'item': '',
                'qty': '',
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_on_post_return_item_qty_added_to_cart(self):
        self.client.cookies = SimpleCookie({'sessionid': self.session.session_key})
        response = self.client.post(
            path=reverse('cart:add-item'),
            data={
                'item': self.product.id,
                'qty': 5,
            }
        )
        data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['added']['item'], self.product.id)
        self.assertEqual(data['added']['qty'], 5)
        self.assertEqual(data['cart_items'], 5)
