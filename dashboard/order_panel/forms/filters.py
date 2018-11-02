import django_filters

from webstore.order.models import Order


class FilterOrdersForm(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = '__all__'
