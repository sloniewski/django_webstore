from datetime import date

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from webstore.core.mixins import TimeStampMixin
from .managers import CategoryManager, ProductManager


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


class Gallery(models.Model):
    """
    Reference table for m2m relation product -> picture.
    Additional information is the picture order.
    """

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
        )

    def __str__(self):
        return '{}. {} - {}'.format(
            self.number,
            self.product.name,
            self.picture.data.name,
        )


class Category(models.Model):
    objects = CategoryManager()

    name = models.CharField(
        max_length=32,
    )
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return 'id: {}, {}'.format(self.pk, self.name)

    @property
    def form_choice(self):
        return self.pk, self.name


class Product(models.Model):
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

    created = models.DateTimeField(
        auto_now_add=True,
    )
    edited = models.DateTimeField(
        auto_now=True,
    )

    weight = models.FloatField(
        help_text='weight in kg',
        default=0,
    )
    width = models.FloatField(
        help_text='width in cm',
        default=0,
    )
    height = models.FloatField(
        help_text='height in cm',
        default=0,
    )
    length = models.FloatField(
        help_text='length in cm',
        default=0,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product-detail', kwargs={'slug': self.slug})

    @property
    def actual_price(self):
        today = timezone.now()
        price = self.prices.filter(valid_from__lte=today).first()
        if price is not None:
            return price.value
        return None

    @property
    def volume(self):
        """
        :return:float, product box volume in cubic meters
        """
        return (self.width * self.height * self.length)*(10**(-6))

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


class Price(models.Model):

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
    created = models.DateTimeField(
        auto_now_add=True,
    )
    edited = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            '-valid_from',
        ]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return 'Price, id: {}, value: {}'.format(object.id, object.value)
