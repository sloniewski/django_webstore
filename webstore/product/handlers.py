from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from webstore.core.utils import random_string

from .models import Product


def generate_slug(instance, model):
    if not instance.slug:
        slug = slugify(instance.name)
        if model.objects.filter(slug=slug).exists():
            slug = slug + random_string(4)
        instance.slug = slug


def generate_number(instance, model, base_number=1):
    if model.objects.count() == 0:
        instance.number = base_number
    else:
        # TODO make is subquery
        last_number = model.objects.all()\
            .aggregate(Max('number'))['number__max']
        instance.number = last_number + 1


@receiver(pre_save, sender=Product)
def pre_save_product_create_slug(sender, instance, *args, **kwargs):
    generate_slug(instance=instance, model=sender)


@receiver(pre_save, sender=Product)
def pre_save_product_create_number(sender, instance, *args, **kwargs):
    generate_number(instance=instance, model=sender, base_number=1015)
