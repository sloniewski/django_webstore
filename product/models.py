from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from . import utils


class Product(models.Model):

    name = models.CharField(
        max_length=32,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
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

    def __str__(self):
        return self.name
