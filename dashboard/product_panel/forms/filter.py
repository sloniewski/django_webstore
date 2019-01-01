import django_filters

from webstore.core.widgets import MaterializeSelectMultiple
from webstore.product.models import Product, Picture, Category


class ProductFilterForm(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='name',
        label='Name',
    )
    price__lte = django_filters.NumberFilter(
        lookup_expr='lte',
        field_name='price',
        label='Price less than'
    )
    price__gte = django_filters.NumberFilter(
        lookup_expr='gte',
        field_name='price',
        label='Price more than'
    )
    category_id = django_filters.ModelMultipleChoiceFilter(
        lookup_expr='name',
        field_name='categories',
        label='Category',
        widget=MaterializeSelectMultiple(),
        queryset=Category.objects.with_products(),
    )
    weight__lte = django_filters.NumberFilter(
        lookup_expr='lte',
        field_name='weight',
        label='weight less than'
    )
    weight__gte = django_filters.NumberFilter(
        lookup_expr='gte',
        field_name='weight',
        label='weight more than'
    )

    class Meta:
        model = Product
        fields = (
            'name',
            'active',
        )


class PictureFilterForm(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='name',
    )

    class Meta:
        model = Picture
        fields = [
            'name'
        ]