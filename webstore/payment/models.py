from django.db import models

from webstore.cash.fields import CashField
from webstore.core.mixins import TimeStampMixin
from webstore.order.models import Order


class PaymentManager(models.Manager):
    def create_for_order(self, order, delivery=None):
        value = order.value + delivery.cost
        payment = self.model(
            order=order,
            value=value,
        )
        payment.save()
        return payment

class Payment(TimeStampMixin, models.Model):
    objects= PaymentManager()

    payed = models.BooleanField(
        default=False,
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.DO_NOTHING,
    )
    method = models.CharField(
        max_length=16,
        choices=[
            ('cr', 'card'),
            ('tr', 'transfer'),
            ('ud', 'upon delivery'),
        ],
        default='tr',
    )

    value = CashField()

    @property
    def user(self):
        return self.order.user
