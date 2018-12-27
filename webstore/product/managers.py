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
            )\
            .annotate(
                is_promo=Subquery(
                    queryset=prices.values('is_promo')[:1],
                    output_field=models.BooleanField(),
                )
            ).annotate(
                promo_message=Subquery(
                    queryset=prices.values('promo_message')[:1],
                    output_field=models.CharField(max_length=255),
                )
            )
        return products


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def with_prices(self):
        return self.get_queryset().with_prices()


class CategoryQuerySet(models.QuerySet):

    def with_products(self):
        return self\
            .annotate(product_count=models.Count('product'))\
            .filter(product_count__gt=0)


class CategoryManager(models.Manager):

    def form_choices(self):
        return [x.form_choice for x in self.get_queryset().all()]

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self.db)

    def with_products(self):
        return self.get_queryset().with_products()


class GalleryManager(models.Manager):

    def safe_bulk_create(self, object_list=[]):
        temp_list = []
        # TODO make this hit database once

        for obj in object_list:
            if not self.model.objects.filter(picture=obj.picture, product=obj.product).exists():
                temp_list.append(obj)
        object_list = temp_list
        return self.bulk_create(object_list)
