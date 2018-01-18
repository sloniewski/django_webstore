from django.test import TestCase

from webstore.cash.db.cash import Cash


class TestCash(TestCase):

    def test_currency(self):
        cash = Cash()
        self.assertEqual(cash.currency, 'EUR')
