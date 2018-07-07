from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model

from webstore.product.models import Product

User = get_user_model()


class CartManager(models.Manager):

    def recive_or_create(self, request):
        session = request.session.session_key
        cart = self.get_queryset().filter(
            session=session).first()
        if cart is None:
            cart = self.model(session=session)
            cart.save()
        return cart

    def get_for_session(self, request):
        session = request.session.session_key
        cart = self.get_queryset().filter(
            session=session).first()
        return cart


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
        return self.product.get_price

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
        # Order of multiplication is important, to call __mul__ of Cash class
        return self.product.get_price * self.quantity

    class Meta:
        unique_together = [
            ('cart', 'product')
        ]


class Cart(models.Model):
    objects = CartManager()

    session = models.CharField(max_length=256, unique=True)

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
            cart_item = CartItem.objects.create(
                product_id=item,
                cart=self,
                quantity=qty,
            )
        return cart_item

    def remove_item(self, item, qty):
        try:
            cart_item = CartItem.objects.get(
                product_id=item,
                cart=self,
            )
            item = cart_item.remove_qty(qty)
            if item is None:
                return None
            return item
        except CartItem.DoesNotExist:
            pass

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
    def weight(self):
        # TODO implement cart weight property
        return 1
