from decimal import Decimal, getcontext

from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

from webstore.product.models import Product

User = get_user_model()


class CartManager(models.Manager):

    def get_for_session(self, request):
        session = request.session.session_key
        cart = self.get_queryset().filter(
            session=session).first()
        return cart


class CartItem(models.Model):
    """
    Reference table for m2m relation cart -> product.
    Stores additional information about quantity.
    """
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [
            ('cart', 'product')
        ]

    @property
    def price(self):
        return self.product.actual_price

    @property
    def weight(self):
        return self.quantity * self.product.weight

    def add_qty(self, qty):
        self.quantity += qty
        self.save()

    def remove_qty(self, qty):
        if self.quantity <= qty:
            self.delete()
            return None
        self.quantity -= qty
        self.save()
        return self

    @property
    def value(self):
        """
        Returns value of order-line.
        """
        getcontext().prec = 4
        # Order of multiplication is important, to call __mul__ of Cash class
        price = self.product.actual_price
        if price:
            return price * self.quantity
        return 0


class Cart(models.Model):
    """
    Cart representation, has unique reference to session_key.
    Does not store items, cart items are m2m relation to cart & product
    """
    objects = CartManager()

    session = models.CharField(
        max_length=255,
        unique=True
    )
    product = models.ManyToManyField(
        Product,
        through=CartItem,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def _get_item(self, item):
        item = CartItem.objects.get(
            product_id=item,
            cart=self,
        )
        return item

    def add_item(self, item, qty):
        try:
            cart_item = self._get_item(item)
            cart_item.add_qty(qty)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product_id=item,
                cart=self,
                quantity=qty,
            )
        return cart_item

    def remove_item(self, item, qty):
        try:
            cart_item = self._get_item(item)
            item = cart_item.remove_qty(qty)
            if item is None:
                return None
            return item
        except CartItem.DoesNotExist:
            pass

    def delete_item(self, item):
        try:
            cart_item = self._get_item(item)
            cart_item.delete()
            return True
        except CartItem.DoesNotExist:
            return True

    @property
    def item_count(self):
        item_count = self.cartitem_set.aggregate(
            Sum('quantity'))['quantity__sum']
        if item_count is None:
            return 0
        return item_count

    def get_items(self):
        return self.cartitem_set.all().select_related('product')

    @property
    def value(self):
        value = 0
        # TODO should be aggregate
        for item in self.cartitem_set.filter(quantity__gte=1):
            value += item.value
        return value

    @property
    def items(self):
        return self.cartitem_set.all().select_related('product')

    @cached_property
    def weight(self):
        weight = 0
        for item in self.items:
            weight += (item.product.weight * item.quantity)
        return weight
