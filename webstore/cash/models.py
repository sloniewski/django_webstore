from decimal import Decimal

from django.conf import settings


class Cash(Decimal):
    """
    Intended as a representation as any amount of monetary value
    through all application code
    """

    currency = settings.WEBSTORE_CURRENCY

    def __add__(self, other, context=None):

        if not isinstance(other, (Cash,)):
            raise ValueError('operation might be performed only with other Cash instance')

        assert self.currency == other.currency, 'adding of two different currencies is not implemented'
        return Cash(super().__add__(other))

    def __mul__(self, other, context=None):
        """
        Implements multiplications for Cash class, multiplication is limited only to integers.
        Multiplying Cash, as it is used to represent price, by something else does not make sense.
        """

        if not isinstance(other, (int,)):
            raise ValueError('operation might be performed only with other Integer instance')
        return Cash(super().__mul__(other))

    def __repr__(self):
        """Represents the number as an instance of Cash."""
        return "Cash('{}')".format(str(self))

    def __str__(self, *args):
        text = super().__str__(*args)
        return '{} {}'.format(
            text,
            self.currency,
        )

