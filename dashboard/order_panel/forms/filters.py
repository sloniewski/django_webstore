import django_filters

from webstore.order.models import Order


class FilterOrdersForm(django_filters.FilterSet):
    email = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        label='User email',
    )
    created_before = django_filters.DateFilter(
        field_name='created',
        lookup_expr='lte',
        label='Created before'
    )
    created_after = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Created after'
    )

    class Meta:
        model = Order
        fields = [
            'uuid',
            'status',
        ]
