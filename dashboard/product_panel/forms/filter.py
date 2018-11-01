import django_filters


from webstore.product.models import Product


class ProductFilterForm(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = '__all__'
