from django.test import TestCase
from django.core.exceptions import ValidationError

from cart import forms
from product.models import Product

import json


class TestAddItemForm(TestCase):
    form_class = forms.AddItemForm

    def test_data_validation(self):
        product = Product.objects.create(name='test')
        form = self.form_class({'item': product.pk, 'qty': '5'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = self.form_class({'item': -1, 'qty': 0},)
        form.full_clean()
        self.assertFalse(form.is_valid())
        self.assertIn('no such product',form.errors['item'].as_json())
        self.assertIn('cannot add 0', form.errors['item'].as_json())
        self.assertIn('cannot add 0', form.errors['qty'].as_json())
