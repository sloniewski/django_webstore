from datetime import date
from urllib.parse import urlencode

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.postgres import indexes
from django.utils.functional import cached_property

from webstore.core.mixins import TimeStampMixin
from .managers import CategoryManager, ProductManager, GalleryManager


class Picture(TimeStampMixin, models.Model):
    name = models.CharField(max_length=32)
    data = models.ImageField(
        upload_to='product_images/',
    )

    def __str__(self):
        return self.data.name

    class Meta:
        ordering = [
            '-created',
        ]
        indexes = [
            models.Index(fields=['name']),
        ]


class Gallery(models.Model):
    """
    Reference table for m2m relation product -> picture.
    Additional information is the picture order.
    """
    objects = GalleryManager()

    product = models.ForeignKey(
        'Product',
        on_delete=models.DO_NOTHING,
    )
    picture = models.ForeignKey(
        Picture,
        on_delete=models.DO_NOTHING,
    )
    number = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ['product', '-number']
        verbose_name = "Gallery Image"
        unique_together = (
            ('product', 'number'),
            ('picture', 'product'),
        )
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['picture']),
        ]

    def __str__(self):
        return '{}. {} - {}'.format(
            self.number,
            self.product.name,
            self.picture.data.name,
        )

    def save(self, *args, **kwargs):
        if self.number is None:
            num = type(self).objects\
                .filter(product=self.product)\
                .aggregate(models.Max('number'))['number__max']
            if num is not None:
                self.number = num['number__max'] + 1
            else:
                self.number = 1
        super().save(*args, **kwargs)


class Category(models.Model):
    objects = CategoryManager()

    name = models.CharField(
        max_length=32,
    )
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return 'id: {}, {}'.format(self.pk, self.name)

    @cached_property
    def form_choice(self):
        return self.pk, self.name

    @cached_property
    def url_encode(self):
        return urlencode({'category_id': self.id})


class Product(TimeStampMixin, models.Model):
    """
    Represents product resource, stores basic information.
    Prices, Pictures and Categories are m2m relations to Product.
    """

    objects = ProductManager()

    name = models.CharField(
        max_length=32,
    )
    active = models.BooleanField(
        default=False,
    )
    picture = models.ManyToManyField(
        Picture,
        through=Gallery,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        null=True,
    )

    number = models.PositiveIntegerField(null=True)

    description = models.TextField(default='description not available')

    stock = models.PositiveIntegerField(default=0)

    categories = models.ManyToManyField(
        Category,
    )
    weight = models.FloatField(
        help_text='weight in kg',
        default=0,
    )

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            indexes.BrinIndex(fields=['weight']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product-detail', kwargs={'slug': self.slug})

    def set_price(self):
        if not hasattr(self, 'price'):
            today = timezone.now()
            price = self.prices.filter(valid_from__lte=today).first()
            if price is not None:
                self.price = price.value
                self.is_promo = price.is_promo
                self.promo_message = price.promo_message
            else:
                self.price = None
                self.is_promo = False
                self.promo_message = None
            return True
        return False

    @property
    def actual_price(self):
        today = timezone.now()
        price = self.prices.filter(valid_from__lte=today).first()
        if price is not None:
            return price.value
        return None

    @property
    def gallery(self):
        return Gallery.objects\
            .select_related('picture')\
            .filter(product_id=self.id)

    @property
    def image(self):
        image = Gallery.objects\
            .filter(product_id=self.id)\
            .select_related('picture')\
            .order_by('number')\
            .first()
        if image:
            return image.picture.data.url
        return None


class Price(TimeStampMixin, models.Model):

    value = models.DecimalField(
        decimal_places=2,
        max_digits=8,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='prices'
    )
    valid_from = models.DateField(
        default=date.today,
        help_text="helps to determine which price is valid at moment of runtime",
    )
    is_promo = models.BooleanField(
        default=False,
    )
    promo_message = models.CharField(
        max_length=255,
        null=True, blank=True,
    )

    class Meta:
        ordering = [
            '-valid_from',
        ]
        indexes = [
            indexes.BrinIndex(fields=['valid_from']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'Price, id: {}, value: {}'.format(object.id, object.value)
