from django.test import TestCase

from webstore.product.models import (
    Product,
    Price,
)


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

    def test_get_latest_price(self):
        product = Product.objects.create(
            name='test product',
        )
        prices = Price.objects.bulk_create([
            Price(value=12.0101, valid_from='2018-01-01', product=product),
            Price(value=45.345, valid_from='2017-04-05', product=product),
            Price(value=78.9999, valid_from='2016-08-12', product=product),
        ])
        self.assertEqual(
            product.get_price,
            '12.0101',
        )

    def test_behaviour_if_no_price_is_set(self):
        product = Product.objects.create(
            name='test product',
        )
        self.assertEqual(
            product.get_price,
            None,
        )
