import django_filters

from .models import Product


class FilterProductsForm(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='name',
    )
    price__lte = django_filters.NumberFilter(
        lookup_expr='lte',
        field_name='price',
        label='Price less than'
    )

    class Meta:
        model = Product
        fields = (
            'name',
        )