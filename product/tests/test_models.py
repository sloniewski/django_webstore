from django.test import TestCase
from django.contrib.auth import get_user_model

from product.models import Product


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

    def test_changing_name_does_not_change_slug(self):
        product = Product(
            name='Red Leicester',
        )
        product.save()

        slug = product.slug
        product.name = 'Norwegian Jarlsberg'
        product.save()
        self.assertEqual(
            product.slug, slug,
            msg='product slug should stay the same after name update',
        )

    def test_get_absolute_url(self):
        product = Product.objects.create(name='The Holy Grail')
        self.assertEqual(
            first='/product/' + product.slug + '/',
            second=product.get_absolute_url(),
        )


class TestUserModel(TestCase):

    def test_user_model_set_properly(self):
        self.assertEqual(
            get_user_model().__name__,
            'WebStoreUser',
            msg='check settings to point to appropriate user model from webstore_user.models'
        )
