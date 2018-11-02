import django_filters

from webstore.payment.models import Payment


class FilterPaymentForm(django_filters.FilterSet):

    class Meta:
        model = Payment
        fields = '__all__'
