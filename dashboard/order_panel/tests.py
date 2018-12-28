from django.shortcuts import reverse
from django.test import TestCase


class TestViews(TestCase):

    def setUp(self):
        pass

    def test_order_list_get(self):
        response = self.client.get(
            reverse(
                viewname='order_panel:order-list',
            )
        )
        self.assertEqual(
            first=response.status_code,
            second=200,
            msg='view returned {} code'.format(response.status_code),
        )
        self.assertTemplateUsed(
            response=response,
            template_name='dashboard/order/order_list.html',
        )
