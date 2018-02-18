from django.db import models

from webstore.core.mixins import TimeStampMixin
from webstore.order.models import Order


class Payment(TimeStampMixin, models.Model):
    payed = models.BooleanField(
        default=False,
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.DO_NOTHING,
    ) 
    method = models.CharField(
        choices = [
            ('cr', 'card'),
            ('tr', 'transfer'),
            ('ud', 'upon delivery'),
        ]
    )

    @property
    def user(self):
        return self.order.user
