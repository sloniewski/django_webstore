from django.urls import reverse, resolve
from django.test import TestCase
from django.utils.text import slugify


class TestProductDetailUrl(TestCase):

    def setUp(self):
        self.test_slug = slugify('The Test Product 123 0')

    def test_reverse(self):
        self.assertEqual(
            first='/product/'+self.test_slug+'/',
            second=reverse('product:product-detail', kwargs={'slug': self.test_slug})
        )

    def test_resolve(self):
        resolver = resolve(reverse('product:product-detail', kwargs={'slug': self.test_slug}))

        self.assertEqual((), resolver.args)
        self.assertEqual({'slug': self.test_slug}, resolver.kwargs)
        self.assertEqual('product', resolver.app_name)
        self.assertEqual('product', resolver.namespace)
