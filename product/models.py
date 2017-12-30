from django.db import models
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
            test_slug = slugify(self.name)
            try:
                Product.objects.get(
                    slug=test_slug
                )
            except models.ObjectDoesNotExist:
                self.slug = test_slug

            self.slug = test_slug + slugify(' '+utils.random_string(4))

        super().save(*args, **kwargs)
