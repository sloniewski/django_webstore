from django.test import TestCase

from cart import forms


class TestAddItemForm(TestCase):
    form_class = forms.AddItemForm

    def test_data_validation(self):
        form = self.form_class({'item': '1', 'qty': '5'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = self.form_class({'item': '', 'qty': ''})
        self.assertFalse(form.is_valid())
