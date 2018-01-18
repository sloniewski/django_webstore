from django.test import TestCase

from webstore.cash.db.cash import Cash
from webstore.cash.db.fields import CashField


class TestCash(TestCase):

    def test_currency(self):
        cash = Cash()
        self.assertEqual(cash.currency, 'EUR')


class TestCashField(TestCase):

    def test_to_python_returns_cash_obj(self):
        field = CashField()
        obj = field.to_python('1.1')
        self.assertEqual(obj, Cash('1.1'))
        self.assertIsInstance(obj, Cash)

    def test_from_db_value_returns_cash_obj(self):
        field = CashField()
        obj = field.from_db_value('1.1')
        self.assertEqual(obj, Cash('1.1'))
        self.assertIsInstance(obj, Cash)

    def test_get_prep_value_returns_str(self):
        field = CashField()
        value = field.get_prep_value(Cash('2.2'))
        self.assertEqual(value, '2.2')
