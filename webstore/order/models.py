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


class OrderManager(models.Manager):

    def create_from_cart(self, cart, user):
        order = self.model.objects.create(
            user=user,
            status=Order.CONFIRMED,
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
    NEW = 'new'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    SHIPPED = 'shipped'
    ORDER_STATUS = (
        (NEW, 'new'),
        (CONFIRMED, 'confirmed'),
        (PAID, 'paid'),
        (SHIPPED, 'shipped'),
    )

    status = models.CharField(
        max_length=32,
        choices=ORDER_STATUS,
    )

    objects = OrderManager()

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
        return self.orderitem_set.all()

    @property
    def item_count(self):
        item_count = self.orderitem_set.aggregate(
            Sum('quantity'))['quantity__sum']
        if item_count is None:
            return 0
        return item_count

    @property
    def value(self):
        value = Cash('0')
        for item in self.orderitem_set.filter(quantity__gte=1):
            value += item.value
        return value

    @property
    def weight(self):
        return self.orderitem_set.aggregate(Sum('weight'))['weight__sum']

    @property
    def volume(self):
        volumes = [x.volume for x in self.orderitem_set.all()]
        return sum(volumes)
