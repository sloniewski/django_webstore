from decimal import Decimal, getcontext
from django.db.models import Transform
from django.db.models.fields import Field
from django.conf import settings

getcontext().prec = 2
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
        if isinstance(other, (int, Decimal)):
            return Cash(super().__mul__(other))
            # raise ValueError('operation might be performed only with other Integer instance')
        elif isinstance(other, (float, str)):
            return Cash(super().__mul__(Decimal(other)))

    def __repr__(self):
        """Represents the number as an instance of Cash."""
        return "Cash('{}')".format(str(self))

    def __str__(self, *args):
        text = super().__str__(*args)
        return '{}'.format(
            text,
        )

    def __len__(self):
        return len(super().__str__())

    @property
    def to_db_value(self):
        return self.__str__()


@Field.register_lookup
class IntegerValue(Transform):
    lookup_name = 'float'  # Used as object.filter(LeftField__int__gte, "777")
    bilateral = True  # To cast both left and right

    def as_sql(self, compiler, connection, function=None, template=None, arg_joiner=None, **extra_context):
        sql, params = compiler.compile(self.lhs)
        sql = 'CAST(%s AS DECIMAL(9,3))' % sql
        return sql, params
