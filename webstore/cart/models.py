from django.db import models
from django.db.models import Sum
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

    def add_qty(self, qty):
        self.quantity += qty
        self.save()

    def get_total_price(self):
        return self.quantity * self.product.get_price

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

    def get_user(self):
        pass