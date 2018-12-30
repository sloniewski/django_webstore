from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from django.test import TestCase

from webstore.order.models import Order
from webstore.payment.models import Payment

User = get_user_model()


class TestIntegrated(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='username')
        self.order = Order.objects.create(user=self.user)
        self.payment = Payment.objects.create(
            payed=False,
            order=self.order,
            value='33.33'
        )

    def test_payment_list_get(self):
        response = self.client.get(
            reverse('payment_panel:payment-list'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/payment/payment_list.html')

    def test_payment_update_view_get(self):
        response = self.client.get(
            reverse(
                'payment_panel:payment-update',
                kwargs={'pk': self.payment.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/payment/payment_update.html')
    
    def test_payment_update_view_post(self):
        response = self.client.post(
            reverse(
                'payment_panel:payment-update',
                kwargs={'pk': self.payment.id},
            ),
            data={'payed': 'on'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('payment_panel:payment-list'))
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.payed, True)
