from enum import Enum
from decimal import Decimal

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse

from webstore.product.models import Product
from webstore.cash.fields import CashField


User = get_user_model()


class OrderItem(models.Model):
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
    price = CashField()

    @property
    def value(self):
        return self.price * self.quantity

    class Meta:
        unique_together = [
            ('order', 'product')
        ]

    def __str__(self):
        return 'product: {}, qty: {}, price: {};'.format(
            self.product.name,
            self.quantity,
            self.price,
        )


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
        for cart_item in cart.cartitem_set.all():
            # TODO should be single query - hit databese one time
            OrderItem.objects.create(
                order=order,
                price=cart_item.price,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )
        return order


class OrderStatusMailFactory:
    order = None
    content_subtype = 'html'
    messages = {
        OrderStatus.AWAITING_PAYMENT.name: {
            'template_name': 'mail/order/awaiting_payment.html',
            'subject': 'Order is awaiting payment',
        },
    }

    def __init__(self, order):
        self.order = order

    def get_mail_obj(self):
        text = render_to_string(
            template_name=self.messages[self.order.status]['template_name'],
            context={
                'order': self.order,
            }
        )
        mail = EmailMessage(
            body=text,
            subject=self.messages[self.order.status]['subject'],
            to=[self.order.user.email]
        )
        mail.content_subtype = self.content_subtype
        return mail


class Order(models.Model):

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

    created = models.DateTimeField(
        auto_now_add=True,
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

    def __str__(self):
        return 'order id: {}, value: {};'.format(self.id, self.value)

    def __repr__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse('order:order-detail', kwargs={'uuid': self.uuid})

    def get_status_mail(self):
        mail_factory = self.mail_manager(order=self)
        return mail_factory.get_mail_obj()

    @property
    def items(self):
        return self.orderitems.all().select_related('product')

    @property
    def value(self):
        value = Decimal('0')
        for item in self.orderitems.filter(quantity__gte=1):
            value += item.value
        return value

    @property
    def weight(self):
        order_items = OrderItem.objects.filter(order_id=self.pk)\
            .select_related('product')
        weight = 0
        for item in order_items:
            weight += (item.quantity * item.product.weight)
        return weight

    @property
    def volume(self):
        volumes = [x.volume for x in self.orderitems.all()]
        return sum(volumes)
