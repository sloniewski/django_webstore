from decimal import Decimal
from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from webstore.product.models import (
    Product,
    Price,
)


class TestProductModel(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='test product',
        )

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
        slug = self.product.slug
        self.product.name = 'Norwegian Jarlsberg'
        self.product.save()
        self.assertEqual(
            self.product.slug, slug,
            msg='product slug should stay the same after name update',
        )

    def test_get_absolute_url(self):
        product = Product.objects.create(name='The Holy Grail')
        self.assertEqual(
            first='/product/' + product.slug + '/',
            second=product.get_absolute_url(),
        )

    def test_get_latest_price(self):
        prices = Price.objects.bulk_create([
            Price(value=12.01, valid_from='2018-01-01', product=self.product),
            Price(value=45.34, valid_from='2017-04-05', product=self.product),
            Price(value=78.99, valid_from='2016-08-12', product=self.product),
        ])
        self.product.set_price()
        self.assertIsInstance(self.product.price, Decimal)
        self.assertEqual(self.product.price,Decimal('12.01'))

    def test_behaviour_if_no_price_is_set(self):
        product = Product.objects.create(
            name='test product',
        )
        product.set_price()
        self.assertEqual(product.price, None)

    def test_price_type(self):

        price = Price.objects.create(
            value=92.9123,
            valid_from='2018-01-01',
            product=self.product
        )
        price.refresh_from_db()
        self.assertIsInstance(
            price.value, Decimal,
            msg='price type is {}'.format(type(price.value)),
        )
        self.assertEqual(price.value, Decimal('92.91'))

    def test_queryset_with_prices(self):
        price = Price.objects.create(
            value='14.01',
            valid_from=now()-timedelta(days=1),
            product=self.product,
            is_promo=True,
            promo_message='best deal',
        )
        product = Product.objects\
            .with_prices()\
            .filter(slug=self.product.slug)\
            .first()

        self.assertEqual(
            product.price, Decimal('14.01'),
            msg='price was {} {}'.format(type(product.price), product.price )
        )
        self.assertEqual(product.is_promo, True)
        self.assertEqual(product.promo_message, 'best deal')
