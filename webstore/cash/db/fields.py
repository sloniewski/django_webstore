from django.db.models import CharField
from django.core.exceptions import ValidationError

from .cash import Cash


class CashField(CharField):
    

    def to_pyhon(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        if not isinstance(value, Cash):
            try:
                value = Cash(value)
            except ValueError:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
            return value
