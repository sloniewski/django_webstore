from django.test import TestCase
from django.contrib.auth import get_user_model

from product.models import Product
from webstore_user.models import WebStoreUser


class TestProductModel(TestCase):

    def test_product_has_unique_slug_created(self):
        test_name = 'the machine that goes \'ping\''
        product_A = Product.objects.create(
            name=test_name,
        )
        product_B = Product.objects.create(
            name=test_name,
        )
        self.assertNotEqual(
            product_A.slug, product_B.slug,
            msg='each product should have an unique slug assigned',
        )


class TestUserModel(TestCase):

    def test_user_model_set_properly(self):
        self.assertEqual(
            get_user_model().__name__,
            'WebStoreUser',
            msg='check settings to point to appropriate user model from webstore_user.models'
        )
