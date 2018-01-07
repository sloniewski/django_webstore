from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

from product.models import Product

User = get_user_model()


class CartManager(models.Manager):

    def get_or_create(self, session_key):
        if self.filter(session=session_key).exists():
            return self.get(session=session_key)
        else:
            return self.create(session=session_key)


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


class Cart(models.Model):
    session = models.ForeignKey(
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

    objects = CartManager

    def add_item(self, item, qty):
        pass

    def get_item_count(self):
        pass

    def get_user(self):
        pass