from decimal import Decimal, getcontext

from django.test import TestCase
from importlib import import_module
from django.conf import settings

from webstore.cart.models import Cart, CartItem
from webstore.product.models import Product, Price
from webstore.core.utils import random_string


class TestCartModel(TestCase):

    def setUp(self):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        self.session = SessionStore()
        self.session.create()
        self.session.save()

        self.cart = Cart.objects.get_or_create(session=self.session)[0]
        self.prod_A = Product.objects.create(name='Red Windsor')
        self.prod_B = Product.objects.create(name='Emmental')
    
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

    def test_remove_item_from_cart(self):
        product = self.create_test_product(price='11')
        item = CartItem.objects.create(product=product, cart=self.cart, quantity=45)
        self.cart.remove_item(product, 4)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 41)

    def test_add_item_to_cart(self):
        self.cart.add_item(self.prod_A.id, 6)
        self.cart.add_item(self.prod_B.id, 7)
        self.assertEqual(
            CartItem.objects.get(product=self.prod_A, cart=self.cart).quantity,
            6,
        )
        self.assertEqual(
            CartItem.objects.get(product=self.prod_B, cart=self.cart).quantity,
            7,
        )

    def test_add_item_dont_create_dupes(self):
        product = self.create_test_product(price='18')
        self.cart.add_item(item=product.id, qty=19)
        self.cart.add_item(item=product.id, qty=11)
        item = CartItem.objects.get(cart=self.cart, product=product)
        self.assertEqual(item.quantity, 30)
        self.assertEqual(self.cart.item_count, 30)

    def test_cart_and_cartitem_value(self):
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
