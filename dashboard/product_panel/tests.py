from decimal import Decimal
from datetime import date
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from webstore.product.models import (
    Product,
    Category,
    Price,
    Picture,
    Gallery,
)


User = get_user_model()


class TestIntegrationUserStaff(TestCase):
    """ test cases for authenticated staff user """

    def setUp(self):
        self.user = User.objects.create_user(username='username', password='1234', is_staff=True)
        self.client.login(username='username', password='1234')

        self.category = Category.objects.create(name='for delete')
        self.delete_this_category = Category.objects.create(name='utensils')
        self.product = Product.objects.create(
            name='The Holy Grail',
        )
        self.delete_this_product = Product.objects.create(
            name='for deletion',
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
        self.delete_this_picture = Picture.objects.create(
            name='for delete', data='/4delete'
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
        self.assertContains(response, self.product.name)

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
            'categories': self.category.id,
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

    def test_product_delete_post(self):
        response = self.client.post(
            reverse(
                'product_panel:product-delete',
                kwargs={'slug': self.delete_this_product.slug},
            ),
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

    def test_product_create_get(self):
        response = self.client.get(
            reverse('product_panel:product-create')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_update.html',
        )

    def test_product_create_post(self):
        data = {
            'name': 'jabberwocky',
            'description': 'mythical creature',
            'weight': 55,
            'width': 7,
            'height': 6,
            'length': 5,
            'categories': self.category.id,
        }
        response = self.client.post(
            reverse(
                'product_panel:product-create',
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

        product = Product.objects.get(**data)
        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.description, data['description'])
        self.assertEqual(product.weight, data['weight'])
        self.assertEqual(product.width, data['width'])
        self.assertEqual(product.height, data['height'])
        self.assertEqual(product.length, data['length'])

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

    def test_product_price_create_post(self):
        data = {
            'value': 76.23,
            'valid_from': date(year=2017, month=4, day=1),
            'is_promo': 'on',
            'promo_message': 'blue monday',
        }
        response = self.client.post(
            reverse(
                'product_panel:product-price-create',
                kwargs={'number': self.product.number},
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",

        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('product_panel:product-price-list', kwargs={'number': self.product.number})
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
        response = self.client.post(
            reverse(
                'product_panel:price-update',
                kwargs={'pk': self.price.pk},
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/product_price_create.html',
        )

    def test_product_price_update_post(self):
        data = {
            'value': '55.55',
            'valid_from': date(year=2016, month=4, day=1),
            'is_promo': 'on',
            'promo_message': 'x',
        }
        response = self.client.post(
            reverse(
                'product_panel:price-update',
                kwargs={'pk': self.price.pk},
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",

        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                'product_panel:product-price-list',
                kwargs={'number': self.product.number},
            )
        )
        self.price.refresh_from_db()
        self.assertEqual(self.price.value, Decimal(data['value']), )
        self.assertEqual(self.price.valid_from, data['valid_from'])
        self.assertEqual(self.price.promo_message, data['promo_message'])
        self.assertEqual(self.price.is_promo, True)

    def test_category_list_get(self):
        response = self.client.get(
            reverse('product_panel:category-list')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/category_list.html',
        )
        self.assertContains(response, self.category.name)

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

    def test_category_update_post(self):
        data = {
            'name': 'aaabbbccc',
            'description': 'aaaaaaaaaaabbbbbbbbbbbb',
        }
        response = self.client.post(
            reverse(
                'product_panel:category-update',
                kwargs={'pk': self.category.pk},
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",

        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_panel:category-list'))
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, data['name'])
        self.assertEqual(self.category.description, data['description'])

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

    def test_category_delete_post(self):
        temp_id = self.delete_this_category.id
        response = self.client.post(
            reverse(
                'product_panel:category-delete',
                kwargs={'pk': self.delete_this_category.pk},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_panel:category-list'))
        with self.assertRaises(Category.DoesNotExist):
            cat = Category.objects.get(id=temp_id)

    def test_category_create_get(self):
        response = self.client.get(
            reverse('product_panel:category-create')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/product/category_create_update.html',
        )

    def test_category_create_post(self):
        data = {
            'name': 'aaabbbccc1111',
            'description': 'aaaaaaaaaaabbbbbbbbbbbb2222',
        }
        response = self.client.post(
            reverse(
                'product_panel:category-create',
            ),
            data=urlencode(data),
            content_type="application/x-www-form-urlencoded",

        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_panel:category-list'))
        category = Category.objects.get(**data)
        self.assertEqual(category.name, data['name'])
        self.assertEqual(category.description, data['description'])

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
        self.assertTemplateUsed(response, 'dashboard/product/picture_delete.html')

    def test_picture_delete_post(self):
        temp_id = self.delete_this_picture.id
        response = self.client.post(
            reverse(
                'product_panel:picture-delete',
                kwargs={'pk': self.delete_this_picture.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_panel:picture-list'))
        with self.assertRaises(Picture.DoesNotExist):
            pic = Picture.objects.get(id=temp_id)

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

    def test_picture_update_post(self):
        response = self.client.post(
            reverse(
                'product_panel:picture-update',
                kwargs={'pk': self.picture.pk}
            ),
            data=urlencode({'name': 'xxxxyyyyzzzz'}),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_panel:picture-list'))
        self.picture.refresh_from_db()
        self.assertEqual(self.picture.name, 'xxxxyyyyzzzz')

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


class TestIntegratedAnonymousUser(TestCase):
    """ test cases for not authenticated user"""

    def setUp(self):
        self.product = Product.objects.create(
            name='test product',
        )
        self.price = Price.objects.create(
            value='11.99',
            valid_from=date(year=2017, month=4, day=1),
            product=self.product,
        )

    def test_product_list_get_302(self):
        test_url = reverse('product_panel:product-list')
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users_panel:login')+'?next='+test_url)

    def test_product_update_get_302(self):
        test_url = reverse(
                'product_panel:product-update',
                kwargs={'slug': self.product.slug},
            )
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users_panel:login')+'?next='+test_url)

    def test_product_delete_get_302(self):
        test_url = reverse(
                'product_panel:product-delete',
                kwargs={'slug': self.product.slug},
            )
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users_panel:login') + '?next=' + test_url)

    def test_product_create_get_302(self):
        test_url = reverse(
                'product_panel:product-create',
            )
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users_panel:login') + '?next=' + test_url)

    def test_product_pricel_list_get_302(self):
        test_url = reverse(
                'product_panel:product-price-list',
                kwargs={'number': self.product.number}
            )
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users_panel:login') + '?next=' + test_url)

    def test_product_price_create_get_302(self):
        test_url = reverse(
                'product_panel:product-price-create',
                kwargs={'number': self.product.number},
            )
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users_panel:login') + '?next=' + test_url)

    def test_product_price_update_get_302(self):
        test_url = reverse(
                'product_panel:price-update',
                kwargs={'pk': self.price.id},
            )
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users_panel:login') + '?next=' + test_url)

