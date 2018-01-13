from django.test import TestCase
from django.contrib.auth import get_user_model

class TestUserModel(TestCase):

    def test_user_model_set_properly(self):
        self.assertEqual(
            get_user_model().__name__,
            'WebStoreUser',
            msg='check settings to point to appropriate user model from \'users\' app'
        )