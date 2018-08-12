from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

from webstore.product.models import Product
from webstore.cash.fields import CashField
from webstore.cash.models import Cash


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

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]


class OrderManager(models.Manager):

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


class Order(models.Model):

    objects = OrderManager()

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

    class Meta:
        ordering = (
            '-created',
        )

    def __str__(self):
        return 'order id: {}, value: {};'.format(self.id, self.value)

    def __repr__(self):
        return self.__str__()

    @property
    def items(self):
        return self.orderitems.all().select_related('product')

    @property
    def item_count(self):
        item_count = self.orderitems.aggregate(
            Sum('quantity'))['quantity__sum']
        if item_count is None:
            return 0
        return item_count

    @property
    def value(self):
        value = Cash('0')
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
        volumes = [x.volume for x in self.orderitem_set.all()]
        return sum(volumes)
