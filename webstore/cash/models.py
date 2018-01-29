from decimal import Decimal

from django.conf import settings


class Cash(Decimal):
    """
    Intended as a representation as any amount of monetary value
    through all application code

    """

    currency = settings.WEBSTORE_CURRENCY

    def __add__(self, other):
        if not isinstance(other, (Cash)):
            raise ValueError('operation might be performed only with other Cash instance')
        return Cash(super().__add__(other))

    def __repr__(self):
        """Represents the number as an instance of Cash."""
        return "Cash('{}')".format(str(self))
