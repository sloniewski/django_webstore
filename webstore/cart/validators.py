from django.core.exceptions import ValidationError


from webstore.product.models import Product


def validate_product_exits(item):
    if not Product.objects.filter(pk=item).exists():
        raise ValidationError(
            message='no such product',
        )


def validate_product_quantity(item, qty):
    return True


def validate_not_null(num):
    if not num > 0:
        raise ValidationError(
            message='cannot add 0',
        )

