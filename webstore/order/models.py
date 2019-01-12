from enum import Enum
from decimal import Decimal

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.functions import Cast
from django.shortcuts import reverse
from django.utils.functional import cached_property

from webstore.order.tasks import AsyncEmailMessage
from webstore.product.models import Product
from webstore.core.mixins import TimeStampMixin


User = get_user_model()


class OrderItemQuerySet(models.QuerySet):

    def with_value(self):
        return self.annotate(
            value=Cast(
                expression=models.F('price') * models.F('quantity'),
                output_field=models.FloatField(),
            )
        )


class OrderItemManager(models.Manager):

    def get_queryset(self):
        return OrderItemQuerySet(self.model, using=self.db)

    def with_value(self):
        return self.get_queryset().with_value()


class OrderItem(models.Model):
    objects = OrderItemManager()

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='orderitems',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
    )

    class Meta:
        unique_together = [
            ('order', 'product')
        ]
        indexes = [
            models.Index(fields=['order', 'product']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return 'product: {}, qty: {}, price: {};'.format(
            self.product.name,
            self.quantity,
            self.price,
        )

    @cached_property
    def value(self):
        if self.price in [None, Decimal('0'), 0]:
            return Decimal('0')
        if self.quantity in [None, Decimal('0'), 0]:
            return Decimal('0')
        return (self.price * self.quantity)


class OrderStatus(Enum):
    AWAITING_PAYMENT = 'awaiting payment'
    SHIPPING = 'shipping'
    CLOSED = 'closed'
    CANCELLED = 'cancelled'

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]


class OrderQuerySet(models.QuerySet):

    def with_properties(self):
        return self.annotate(item_count=models.Count('orderitems'))


class OrderManager(models.Manager):

    def get_queryset(self):
        return OrderQuerySet(self.model, using=self.db)

    def with_properties(self):
        return self.get_queryset().with_properties()

    def create_from_cart(self, cart, user):
        order = self.model.objects.create(
            user=user,
            status=OrderStatus.AWAITING_PAYMENT.name,
        )
        OrderItem.objects.bulk_create(
            [OrderItem(order=order, price=cart_item.price,
                       product=cart_item.product, quantity=cart_item.quantity,)
             for cart_item in cart.cartitem_set.all()]
        )
        cart.delete()
        return order


class OrderStatusMailFactory:
    order = None
    content_subtype = 'html'
    messages = {
        OrderStatus.AWAITING_PAYMENT.name: {
            'template_name': 'mail/order/awaiting_payment.html',
            'subject': 'Order is awaiting payment',
        },
        OrderStatus.SHIPPING.name: {
            'template_name': 'mail/order/shipping.html',
            'subject': 'Order is under preparation',
        },
        OrderStatus.CLOSED.name: {
            'template_name': 'mail/order/closed.html',
            'subject': 'Your order was shipped',
        },
        OrderStatus.CANCELLED.name: {
            'template_name': 'mail/order/cancelled.html',
            'subject': 'Your order was cancelled',
        },
    }

    def __init__(self, order):
        self.order = order

    def get_mail_obj(self):
        text = render_to_string(
            template_name=self.messages[self.order.status]['template_name'],
            context={
                'order': self.order,
                'user': self.order.user,
            }
        )
        mail = AsyncEmailMessage(
            body=text,
            subject=self.messages[self.order.status]['subject'],
            to=[self.order.user.email],
        )
        mail.content_subtype = self.content_subtype
        return mail


class Order(TimeStampMixin, models.Model):

    objects = OrderManager()
    mail_manager = OrderStatusMailFactory

    status = models.CharField(
        max_length=32,
        choices=OrderStatus.choices(),
        default=OrderStatus.AWAITING_PAYMENT.name,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    uuid = models.CharField(
        max_length=32,
        unique=True,
        null=True,
    )

    class Meta:
        ordering = (
            '-created',
        )
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['uuid']),
        ]

    def __str__(self):
        return 'order id: {}, value: {};'.format(self.uuid, self.value)

    def __repr__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse('order:order-detail', kwargs={'uuid': self.uuid})

    def get_status_mail(self):
        mail_factory = self.mail_manager(order=self)
        return mail_factory.get_mail_obj()

    @property
    def items(self):
        return self.orderitems.all().with_value().select_related('product')

    @cached_property
    def value(self):
        value = self.orderitems\
            .all()\
            .with_value()\
            .aggregate(total_value=models.Sum('value'))
        total_value = value['total_value']
        if total_value in [0, None, False]:
            total_value = 0
        return round(Decimal(total_value), 2) + self.delivery.cost

    @cached_property
    def weight(self):
        order_items = OrderItem.objects.filter(order_id=self.pk)\
            .select_related('product')
        weight = 0
        for item in order_items:
            weight += (item.quantity * item.product.weight)
        return weight
