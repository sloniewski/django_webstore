from decimal import Decimal

from django.db import models
from django.db.models import Sum, F
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

from webstore.product.models import Product

User = get_user_model()


class CartManager(models.Manager):
    pass


class CartItem(models.Model):
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()

    @property
    def price(self):
        return self.product.get_price()

    def add_qty(self, qty):
        self.quantity += qty
        self.save()

    def get_item_value(self):
        """
        Returns value of order-line.

        """
        # Order of multiplication is important, we want to call __mul__ of Cash class
        return self.product.get_price * self.quantity

    class Meta:
        unique_together = [
            ('cart', 'product')
        ]


class Cart(models.Model):
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
    )

    product = models.ManyToManyField(
        Product,
        through=CartItem,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    def add_item(self, item, qty):
        try:
            cart_item = CartItem.objects.get(
                product_id=item,
                cart=self,
            )
            cart_item.add_qty(qty)
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                product_id=item,
                cart=self,
                quantity=qty,
            )

    def get_item_count(self):
        return self.cartitem_set.aggregate(Sum('quantity'))['quantity__sum']

    def get_items(self):
        return self.cartitem_set.all()

    def get_cart_value(self):
        value = 0
        for item in self.cartitem_set.filter(quantity__gte=1):
            value += item.get_item_value()
        return value
