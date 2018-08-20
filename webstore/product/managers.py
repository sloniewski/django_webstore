from django.db import models


class ProductQuerySet(models.QuerySet):

    def with_prices(self):
        pass


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def with_prices(self):
        return self.raw(
            'SELECT *,'
                '(SELECT value FROM product_price '
                'where product_price.valid_from <= now() '
                'and  product_price.product_id = product_product.id '
                'order by product_price.valid_from desc limit 1) as this_price '
            'from product_product;'
        )


class CategoryManager(models.Manager):

    def form_choices(self):
        return [x.form_choice for x in self.get_queryset().all()]
