import django_filters


from webstore.product.models import Product, Picture


class ProductFilterForm(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = '__all__'


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