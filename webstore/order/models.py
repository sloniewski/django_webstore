from django.contrib.auth import get_user_model
from django.db import models

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
        order = self.model.objects.create(user=user)
        for cart_item in cart.cartitem_set.all():
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
        ordering= (
            '-created',
        )

    @property
    def items(self):
        return self.orderitem_set.all()

    @property
    def value(self):
        value = Cash('0')
        for item in self.orderitem_set.filter(quantity__gte=1):
            value += item.value
        return value
