from django.shortcuts import reverse, get_object_or_404
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    DeleteView,
    CreateView,
    DetailView,
)

from django_filters.views import FilterView
from webstore.product.models import Product, Price
from webstore.payment.models import Payment, PaymentStatus
from webstore.delivery.models import Delivery, DeliveryStatus

from .forms import (
    AddProductForm,
    FilterDelieriesForm,
    DeliveryUpdateForm,
)


class DashboardWelcomeView(TemplateView):
    """
    Generic TemplateView,
    **Template:**
    :template:`dasboard/base_dashboard.html`
    """
    template_name = 'dashboard/base_dashboard.html'


class DeliveryListView(FilterView):
    model = Delivery
    template_name = 'dashboard/delivery/delivery_list.html'
    filter_form_class = FilterDelieriesForm

    def get_queryset(self, *args, **kwargs):
        status = self.request.resolver_match.kwargs.get('status').upper()
        status = DeliveryStatus[status].name
        if status is not None:
            queryset = super().get_queryset(*args, **kwargs)
            queryset = queryset.filter(status=status)
            return queryset
        else:
            return super().get_queryset(*args, **kwargs)


class DeliveryUpdateView(UpdateView):
    model = Delivery
    template_name = 'dashboard/delivery/delivery_update.html'
    form_class = DeliveryUpdateForm
    success_url = '/dashboard/delivery/list/shipped'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        order = Order.objects.filter(delivery__pk=pk).first()
        context_data.update({'order': order})
        return context_data

