from django.test import TestCase
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.models import Session

from cart.models import Cart, CartItem
from product.models import Product

from unittest import skip


class TestCartModel(TestCase):

    def setUp(self):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        self.session = SessionStore()
        self.session.create()
        self.session.save()

    def test_add_item_to_cart(self):
        session = Session.objects.get(pk=self.session.session_key)
        cart = Cart.objects.create(session=session)
        prod_A = Product.objects.create(name='Red Windsor')
        prod_B = Product.objects.create(name='Emmental')
        cart.add_item(prod_A.id, 6)
        cart.add_item(prod_B.id, 7)
        cart.add_item(prod_A.id, 19)

        self.assertEqual(cart.get_item_count(), 32)
        self.assertEqual(
            first=CartItem.objects.get(
                        product=prod_A,
                        cart=cart,
                ).quantity,
            second=25
        )
        self.assertEqual(
            first=CartItem.objects.get(
                    product=prod_B,
                    cart=cart,
                ).quantity,
            second=7
        )

    def test_get_or_create_cart(self):
        cart_A = Cart.objects.get_or_create(session_id=self.session.session_key)[0]
        cart_B = Cart.objects.get_or_create(session_id=self.session.session_key)[0]
        self.session.create()
        cart_C = Cart.objects.get_or_create(session_id=self.session.session_key)[0]

        self.assertEqual(cart_A.session.session_key, cart_B.session.session_key)
        self.assertNotEqual(cart_A.session.session_key, cart_C.session.session_key)

    def test_get_cart_items(self):
        prod_A = Product.objects.create(name='Red Windsor')
        prod_B = Product.objects.create(name='Emmental')
        cart = Cart.objects.create(session=self.session.session_key)
        cart.add_item(prod_A.id, 6)
        cart.add_item(prod_B.id, 7)
        cart_items = cart.get_items()

        self.assertIn(prod_A, cart_items)
        self.assertIn(prod_B, cart_items)
