from enum import Enum

from django.db import models
from django.utils import timezone

from webstore.cash.fields import CashField
from webstore.core.mixins import TimeStampMixin
from webstore.order.models import Order


class PaymentStatus(Enum):
    OPEN = 'open'
    DELAYED = 'delayed'
    CLOSED = 'closed'

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def active(cls):
        return [x.name for x in cls if x.name != 'CLOSED']


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
    objects = PaymentManager()

    payed = models.BooleanField(
        default=False,
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.DO_NOTHING,
        related_name='payment',
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

    status = models.CharField(
        max_length=16,
        choices=PaymentStatus.choices(),
        default=PaymentStatus.OPEN.name,
    )

    value = CashField()

    def __str__(self):
        return 'User {}, value: {}'.format(self.order.user, self.value)

    def __repr__(self):
        return self.__str__()

    @property
    def user(self):
        return self.order.user

    @property
    def days_outstanding(self):
        now = timezone.now()
        return (now - self.created).days
