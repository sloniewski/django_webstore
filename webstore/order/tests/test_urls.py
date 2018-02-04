from django.urls import reverse, resolve
from django.test import TestCase


class TestOrderUrls(TestCase):

    def test_reverse(self):
        self.assertEqual(
            first='/order/detail/1',
            second=reverse('order:order-detail', kwargs={'pk': 1})
        )

    def test_resolve(self):
        resolver = resolve(reverse('order:order-detail', kwargs={'pk': 1}))
        self.assertEqual((), resolver.args)
        self.assertEqual({'pk': 1}, resolver.kwargs)
        self.assertEqual('order', resolver.app_name)
        self.assertEqual('order', resolver.namespace)
