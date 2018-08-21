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
        products = self.annotate(
            actual_price=Subquery(
                queryset=prices.values('value')[:1],
                output_field=models.FloatField(),
            ))
        return products


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def with_prices(self):
        return self.get_queryset().with_prices()


class CategoryManager(models.Manager):

    def form_choices(self):
        return [x.form_choice for x in self.get_queryset().all()]
