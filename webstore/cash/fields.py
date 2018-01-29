from django.db.models import CharField
from django.core.exceptions import ValidationError

from .models import Cash


class CashField(CharField):
    max_length = 12

    def __init__(self, *args, **kwargs):
        # sets max_length=32, to fool the defalut charfield validator
        kwargs.setdefault('max_length', 32)
        super().__init__(*args, **kwargs)

    def parse_cash(self, value):
        try:
            value = Cash(value)
        except ValueError:
            raise ValidationError
        return value

    def from_db_value(self, value, expression=None, connection=None):
        if value is None:
            return value
        return self.parse_cash(value)

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        return self.parse_cash(value)

    def get_prep_value(self, value):
        return str(value)
