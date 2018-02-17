from datetime import date

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from webstore.cash import fields
from . import utils


class Product(models.Model):

    name = models.CharField(
        max_length=32,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )

    description = models.TextField(default='description not available')

    stock = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(
        auto_now_add=True,
    )
    edited = models.DateTimeField(
        auto_now=True,
    )

    weight = models.FloatField()
    width = models.FloatField(
        help_text='width in cm',
    )
    height = models.FloatField(
        help_text='height in cm',
    )
    length = models.FloatField(
        help_text='length in cm',
    )

    def save(self, *args, **kwargs):
        if not all([self.slug, self.pk]):
            slug = slugify(self.name)
            if not Product.objects.filter(slug=slug).exists():
                self.slug = slug
            else:
                self.slug = slugify(self.name+' '+utils.random_string(4))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:product-detail', kwargs={'slug': self.slug})

    @property
    def get_price(self):
        price = self.price_set.first()
        if price is not None:
            return price.value
        return None

    @property
    def volume(self):
        """
        :return:product box volume in cubic meters
        """
        return (self.width * self.height * self.length)*(10**(-6))

    def __str__(self):
        return self.name


class Price(models.Model):

    value = fields.CashField(
        help_text="returns instance of Cash"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
    )
    valid_from = models.DateField(
        default=date.today,
        help_text="helps to determine which price is valid at moment of runtime"
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
