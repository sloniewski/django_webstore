
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from webstore.core.mixins import TimeStampMixin
from webstore.order.models import Order, OrderStatus


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
        on_delete=models.CASCADE,
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
    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    class Meta:
        indexes = [
            models.Index(fields=['order']),
        ]

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
        if self.order.status == OrderStatus.AWAITING_PAYMENT.name:
            return (now - self.created).days
        return '-'

    @cached_property
    def status(self):
        if self.order.status == OrderStatus.AWAITING_PAYMENT.name:
            return 'open'
        else:
            return 'closed'
