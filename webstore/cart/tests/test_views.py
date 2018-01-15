from django.shortcuts import reverse
from django.test import TestCase

from webstore.product.models import Product

import json


class TestAddItemView(TestCase):
    '''
    Tests for view responsible for adding items to cart
    ''' 

    def test_get_raises_404(self):
        response = self.client.get(
            reverse('cart:add-item'),
        )
        self.assertEqual(response.status_code, 404)

    def test_on_post_return_400_when_params_missing(self):
        response = self.client.post(
            path=reverse('cart:add-item'),
            data={
                'item': '',
                'qty': '',
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_on_post_return_item_qty_added_to_cart(self):
        product = Product.objects.create(name='Mint Chocolate')
        response = self.client.post(
            path=reverse('cart:add-item'),
            data={
                'item': product.id,
                'qty': 5,
            }
        )
        data = json.loads(response.content.decode("utf-8"))


        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['added']['item'], product.id)
        self.assertEqual(data['added']['qty'], 5)
        self.assertEqual(data['cart_items'], 5)


class TestCartSummaryView(TestCase):

    def test_cart_summary_view(self):
        response = self.client.get(
            path=reverse('cart:cart-summary'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=response,
            template_name='cart/cart_summary',
        )
