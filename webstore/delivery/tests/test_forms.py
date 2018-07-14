from django.test import TestCase

from webstore.delivery.forms import ChooseDeliveryForm


class TestChooseDeliveryForm(TestCase):

    def setUp(self):
        self.form = ChooseDeliveryForm()
