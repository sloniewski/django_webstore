from datetime import date
from urllib.parse import urlencode

from django.shortcuts import reverse
from django.test import TestCase

from webstore.product.models import (
    Product,
    Category,
    Price,
    Picture,
    Gallery,
)


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
        self.picture = Picture.objects.create(
            name='clay bowl', data='/test'
        )
        self.gallery = Gallery.objects.create(
            picture=self.picture,
            product=self.product,
            number=1,
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

    def test_product_update_post(self):
        data = {
            'name': 'changed_name',
            'active': 'on',
            'description': 'altered description',
            'weight': 99,
            'width': 5,
            'height': 5,
            'length': 5,
            'categories': 1,
            'submit': 'submit',
        }
        response = self.client.post(
            reverse(
                'product_panel:product-update',
                kwargs={'slug': self.product.slug},
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(
            first=response.status_code,
            second=302,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertEqual(
            first=response.url,
            second=reverse('product_panel:product-list')
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'changed_name')
        self.assertEqual(self.product.description, 'altered description')
        self.assertEqual(self.product.weight, 99)
        self.assertEqual(self.product.width, 5)
        self.assertEqual(self.product.height, 5)
        self.assertEqual(self.product.length, 5)
        self.assertEqual(self.product.active, True)

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

    def test_category_list_get(self):
        response = self.client.get(
            reverse('product_panel:category-list')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/category_list.html',
        )

    def test_category_update_get(self):
        response = self.client.get(
            reverse(
                'product_panel:category-update',
                kwargs={'pk': self.category.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/category_create_update.html',
        )

    def test_category_delete_get(self):
        response = self.client.get(
            reverse(
                'product_panel:category-delete',
                kwargs={'pk': self.category.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/generic_delete.html',
        )

    def test_category_create_get(self):
        response = self.client.get(
            reverse('product_panel:category-create')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/category_create_update.html',
        )

    def test_picture_list_get(self):
        response = self.client.get(
            reverse('product_panel:picture-list')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/picture_list.html',
        )

    def test_picture_create_get(self):
        response = self.client.get(
            reverse('product_panel:picture-create')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/picture_create.html',
        )

    def test_picture_delete_get(self):
        response = self.client.get(
            reverse(
                'product_panel:picture-delete',
                kwargs={'pk': self.picture.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/picture_delete.html',
        )

    def test_picture_update_get(self):
        response = self.client.get(
            reverse(
                'product_panel:picture-update',
                kwargs={'pk': self.picture.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/picture/picture_update.html',
        )

    def test_product_gallery_get(self):
        response = self.client.get(
            reverse(
                'product_panel:product-gallery',
                kwargs={'slug': self.product.slug}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_gallery.html',
        )

    def test_product_gallery_upload_get(self):
        response = self.client.get(
            reverse(
                'product_panel:product-gallery-upload',
                kwargs={'slug': self.product.slug}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_gallery_upload.html',
        )

    def test_product_gallery_add_get(self):
        response = self.client.get(
            reverse(
                'product_panel:product-gallery-add',
                kwargs={'slug': self.product.slug}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_gallery_add.html',
        )
