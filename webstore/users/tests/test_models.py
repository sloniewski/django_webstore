from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserModel(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_user_model_set_properly(self):
        self.assertEqual(
            self.user_model.__name__,
            'CustomUser',
            msg='check settings to point to appropriate user model from \'users\' app'
        )
