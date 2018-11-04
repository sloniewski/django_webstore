from decimal import Decimal, getcontext

from django.test import TestCase
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.models import Session

from webstore.cart.models import Cart, CartItem
from webstore.cash.models import Cash
from webstore.product.models import Product, Price
from webstore.core.utils import random_string


class TestCartModel(TestCase):

    def setUp(self):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        self.session = SessionStore()
        self.session.create()
        self.session.save()
    
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

    def test_add_item_to_cart(self):
        session = Session.objects.get(pk=self.session.session_key)
        cart = Cart.objects.create(session=session)
        prod_A = Product.objects.create(name='Red Windsor')
        prod_B = Product.objects.create(name='Emmental')
        cart.add_item(prod_A.id, 6)
        cart.add_item(prod_B.id, 7)
        cart.add_item(prod_A.id, 19)

        self.assertEqual(cart.item_count, 32)
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
        # Create a few sessions to test if get_or_create is idempotent due to issues with MySql
        cart_A = Cart.objects.get_or_create(session=self.session.session_key)[0]
        cart_B = Cart.objects.get_or_create(session=self.session.session_key)[0]
        self.session.create()
        cart_C = Cart.objects.get_or_create(session=self.session.session_key)[0]
        
        self.assertEqual(
            cart_A.session,
            cart_B.session,
        )
        self.assertNotEqual(cart_A.session, cart_C.session)

    def test_cart_and_cartitem_total(self):
        getcontext().prec = 4
        cart = Cart.objects.get_or_create(session=self.session.session_key)[0]
        prod_A = self.create_test_product(price='2.71')
        prod_B = self.create_test_product(price='6.02')
        cart.add_item(prod_A.id, 6)
        cart.add_item(prod_B.id, 7)

        value = cart.value
        self.assertEqual(value, Decimal('58.40'))

        item_A = cart.cartitem_set.get(product=prod_A)
        self.assertEqual(item_A.value, Decimal('16.26'))
        self.assertIsInstance(item_A.value, Decimal)

        item_B = cart.cartitem_set.get(product=prod_B)
        self.assertEqual(item_B.value, Decimal('42.14'))
        self.assertIsInstance(item_B.value, Decimal)
