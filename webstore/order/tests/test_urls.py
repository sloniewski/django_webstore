from django.urls import reverse, resolve
from django.test import TestCase


class TestOrderUrls(TestCase):

    def test_reverse(self):
        self.assertEqual(
            first='/order/summary/',
            second=reverse('order:summary', kwargs={})
        )

    def test_resolve(self):
        resolver = resolve(reverse('order:summary', kwargs={}))
        self.assertEqual((), resolver.args)
        self.assertEqual({}, resolver.kwargs)
        self.assertEqual('cart', resolver.app_name)
        self.assertEqual('cart', resolver.namespace)
