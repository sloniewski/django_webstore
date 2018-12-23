from django.db import models
from django.db.models import OuterRef, Subquery
from django.utils import timezone


# from django.apps import apps
# Price = apps.get_model('webstore.product', 'Price')
# raises django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.


class ProductQuerySet(models.QuerySet):

    def with_prices(self):
        # TODO circular import workaround
        from .models import Price
        prices = Price.objects\
            .filter(product=OuterRef('pk'), valid_from__lte=timezone.now())\
            .order_by('-valid_from')
        products = self\
            .annotate(
                price=Subquery(
                    queryset=prices.values('value')[:1],
                    output_field=models.DecimalField(),
                )
            )
        return products


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def with_prices(self):
        return self.get_queryset().with_prices()


class CategoryManager(models.Manager):

    def form_choices(self):
        return [x.form_choice for x in self.get_queryset().all()]


class GalleryManager(models.Manager):

    def safe_bulk_create(self, object_list=[]):
        temp_list = []
        # TODO make this hit database once

        for obj in object_list:
            if not self.model.objects.filter(picture=obj.picture, product=obj.product).exists():
                temp_list.append(obj)
        object_list = temp_list
        return self.bulk_create(object_list)
