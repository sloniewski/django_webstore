import django_filters

from webstore.core.widgets import MaterializeSelectMultiple

from .models import Product, Category


class FilterProductsForm(django_filters.FilterSet):
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

    class Meta:
        model = Product
        fields = (
            'name',
        )
