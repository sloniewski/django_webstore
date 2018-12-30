from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase


User = get_user_model()


class TestViews(TestCase):

    def setUp(self):
        self.user_staff = User.objects.create(username='staff', is_staff=True)
        self.user_client = User.objects.create(username='client', is_staff=False)

    def test_staff_list_get(self):
        response = self.client.get(reverse('users_panel:staff-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/users/staff_list.html')
        self.assertContains(response, self.user_staff.username)

    def test_client_list_get(self):
        response = self.client.get(reverse('users_panel:client-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/users/client_list.html')
        self.assertContains(response, self.user_client.username)
