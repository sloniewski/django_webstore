from django.views import generic
from django_filters.views import FilterView

from webstore.order.models import Order
from webstore.payment.models import Payment

from .forms import FilterPaymentForm, UpdatePaymentForm


class PaymentListView(FilterView):
    model = Payment
    template_name = 'dashboard/payment/payment_list.html'
    filter_form_class = FilterPaymentForm
    paginate_by = 20
    strict = False

    def get_queryset(self):
        return self.model.objects.all().select_related('order')


class PaymentUpdateView(generic.UpdateView):
    model = Payment
    template_name = 'dashboard/payment/payment_update.html'
    form_class = UpdatePaymentForm
    success_url = '/dashboard/payment/list/open'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        order = Order.objects.filter(payment__pk=pk).first()
        context_data.update({'order': order})
        return context_data
