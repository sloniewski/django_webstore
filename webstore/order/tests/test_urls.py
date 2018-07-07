from django.urls import reverse, resolve
from django.test import TestCase


class TestOrderDetailUrl(TestCase):

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


class TestOrderConfirmUrl(TestCase):

    def test_reverse(self):
        self.assertEqual(
            first='/order/confirm/',
            second=reverse('order:order-confirm')
        )

    def test_resolve(self):
        resolver = resolve(reverse('order:order-confirm'))
        self.assertEqual((), resolver.args)
        self.assertEqual({}, resolver.kwargs)
        self.assertEqual('order', resolver.app_name)
        self.assertEqual('order', resolver.namespace)


class TestOrderSummaryUrl(TestCase):

    def test_reverse(self):
        self.assertEqual(
            first='/order/summary/1',
            second=reverse('order:order-summary', kwargs={'pk': 1})
        )

    def test_resolve(self):
        resolver = resolve(reverse('order:order-summary', kwargs={'pk': 1}))
        self.assertEqual((), resolver.args)
        self.assertEqual({'pk': 1}, resolver.kwargs)
        self.assertEqual('order', resolver.app_name)
        self.assertEqual('order', resolver.namespace)


class TestOrderListUrl(TestCase):

    def test_reverse(self):
        self.assertEqual(
            first='/order/list/',
            second=reverse('order:order-list')
        )

    def test_resolve(self):
        resolver = resolve(reverse('order:order-list'))
        self.assertEqual((), resolver.args)
        self.assertEqual({}, resolver.kwargs)
        self.assertEqual('order', resolver.app_name)
        self.assertEqual('order', resolver.namespace)
