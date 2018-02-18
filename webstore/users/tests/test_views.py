from django.shortcuts import reverse
from django.test import TestCase

from webstore.users.views import (
    UsersLoginView,
)


class TestUsersViews(TestCase):

    def test_login_view(self):
        response = self.client.get(reverse("users:login"))

        self.assertEqual(200, response.status_code)
        self.assertEqual(UsersLoginView.as_view().__name__, response.resolver_match.func.__name__)
        self.assertTemplateUsed(response, template_name='users/login.html')