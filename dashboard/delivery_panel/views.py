from django.shortcuts import reverse
from django.views import generic
from django.contrib import messages

from django_filters.views import FilterView

from webstore.delivery.models import Delivery, DeliveryPricing
from webstore.order.models import Order
from dashboard.main.mixins import StaffOnlyMixin

from .forms import (
    DeliveryUpdateForm,
    FilterDeliveriesForm,
    DeliveryPricingForm,
)


class DeliveryListView(StaffOnlyMixin, FilterView):
    model = Delivery
    template_name = 'dashboard/delivery/delivery_list.html'
    filterset_class = FilterDeliveriesForm
    strict = False
    paginate_by = 20


class DeliveryUpdateView(StaffOnlyMixin, generic.UpdateView):
    model = Delivery
    template_name = 'dashboard/delivery/delivery_update.html'
    form_class = DeliveryUpdateForm
    success_url = '/dashboard/delivery/list/shipped'

    def get_context_data(self, **kwargs):
        context_data = super(DeliveryUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        order = Order.objects.filter(delivery__pk=pk).first()
        context_data.update({'order': order})
        return context_data

    def get_success_url(self):
        messages.success(self.request, 'Delivery for order {} updated'.format(self.object.order.uuid))
        return reverse('delivery_panel:delivery-list')


class DeliveryDetailView(StaffOnlyMixin, generic.DetailView):
    model = Delivery
    template_name = 'dashboard/delivery/delivery_detail.html'


class DeliveryPricingListView(StaffOnlyMixin, generic.ListView):
    model = DeliveryPricing
    template_name = 'dashboard/delivery/delivery_option_list.html'


class DeliveryPricingUpdateView(StaffOnlyMixin, generic.UpdateView):
    model = DeliveryPricing
    template_name = 'dashboard/delivery/delivery_option_update.html'
    form_class = DeliveryPricingForm

    def get_success_url(self):
        messages.success(self.request, 'Delivery option {} updated'.format(self.object.name))
        return reverse('delivery_panel:delivery-option-list')


class DeliveryPricingCreateView(StaffOnlyMixin, generic.CreateView):
    model = DeliveryPricing
    form_class = DeliveryPricingForm
    template_name = 'dashboard/delivery/delivery_option_update.html'

    def get_success_url(self):
        messages.success(self.request, 'Delivery option {} created'.format(self.object.name))
        return reverse('delivery_panel:delivery-option-list')


class DeliveryPricingDeleteView(StaffOnlyMixin, generic.DeleteView):
    model = DeliveryPricing
    template_name = 'dashboard/generic_delete.html'

    def get_success_url(self):
        messages.info(self.request, 'Delivery option {} deleted'.format(self.object.name))
        return reverse('delivery_panel:delivery-option-list')
