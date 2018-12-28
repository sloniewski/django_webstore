from datetime import date

from django.shortcuts import reverse
from django.test import TestCase

from webstore.product.models import Product, Category, Price


class TestViews(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='utensils')
        self.product = Product.objects.create(
            name='The Holy Grail',
        )
        self.product.categories.add(self.category)
        self.price = Price.objects.create(
            value=11.11,
            valid_from=date(year=2017, month=1, day=1),
            product=self.product,
        )

    def test_product_list_get(self):
        response = self.client.get(
            reverse('product_panel:product-list')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_list.html',
        )

    def test_product_update_get(self):
        response = self.client.get(
            reverse(
                'product_panel:product-update',
                kwargs={'slug': self.product.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_update.html',
        )

    def test_product_delete_get(self):
        response = self.client.get(
            reverse(
                'product_panel:product-delete',
                kwargs={'slug': self.product.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_delete.html'
        )

    def test_product_create_get(self):
        response = self.client.get(
            reverse('product_panel:product-create')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_update.html',
        )

    def test_product_price_create_get(self):
        response = self.client.get(
            reverse(
                'product_panel:product-price-create',
                kwargs={'number': self.product.number},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_price_create.html',
        )

    def test_product_price_list_get(self):
        response = self.client.get(
            reverse(
                'product_panel:product-price-list',
                kwargs={'number': self.product.number},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_price_list.html',
        )

    def test_product_price_update_get(self):
        response = self.client.get(
            reverse(
                'product_panel:price-update',
                kwargs={'pk': self.price.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_price_create.html',
        )
