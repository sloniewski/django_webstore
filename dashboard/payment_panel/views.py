from django.views import generic
from django_filters.views import FilterView
from django.shortcuts import reverse

from webstore.order.models import Order
from webstore.payment.models import Payment

from .forms import FilterPaymentForm, UpdatePaymentForm


class PaymentListView(FilterView):
    http_method_names = ['get', 'head', 'options']
    template_name = 'dashboard/payment/payment_list.html'
    filterset_class = FilterPaymentForm
    paginate_by = 20
    strict = False
    model = Payment


    def get_queryset(self):
        return self.model.objects.all().select_related('order')


class PaymentUpdateView(generic.UpdateView):
    model = Payment
    template_name = 'dashboard/payment/payment_update.html'
    form_class = UpdatePaymentForm
    success_url = '/dashboard/payment/list/open'

    def dispatch(self, request, *args, **kwargs):
        pk = request.resolver_match.kwargs.get('pk')
        self.order = Order.objects.filter(payment__pk=pk).first()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'order': self.order})
        return context_data

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'order': self.order})
        return kwargs

    def get_success_url(self):
        return reverse('payment_panel:payment-list')
