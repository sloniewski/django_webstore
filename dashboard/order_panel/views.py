from django.views import generic
from django.shortcuts import reverse, get_object_or_404
from django.db.models import Count
from django.contrib import messages

from django_filters.views import FilterView

from dashboard.main.mixins import StaffOnlyMixin
from webstore.order.models import Order, OrderItem
from .forms import (
    FilterOrdersForm,
    OrderUpdateForm,
    item_formset,
)


class OrderListView(StaffOnlyMixin, FilterView):
    model = Order
    template_name = 'dashboard/order/order_list.html'
    filterset_class = FilterOrdersForm
    strict = False
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.all()\
            .select_related('payment')\
            .prefetch_related('orderitems')\
            .annotate(num_items=Count('orderitems'))


class OrderUpdateView(StaffOnlyMixin, generic.UpdateView):
    model = Order
    template_name = 'dashboard/order/order_update.html'
    form_class = OrderUpdateForm

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(self.model, uuid=uuid)

    def get_success_url(self):
        return reverse('order_panel:order-list')


class OrderEditView(StaffOnlyMixin, generic.FormView):
    form_class = item_formset
    template_name = 'dashboard/order/order_item_edit.html'

    def dispatch(self, request, *args, **kwargs):
        uuid = request.resolver_match.kwargs.get('uuid')
        self.order = get_object_or_404(Order, uuid=uuid)
        return super(OrderEditView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.order})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(OrderEditView, self).get_context_data(**kwargs)
        context.update({'order': self.order})
        return context

    def form_valid(self, form):
        form.save()
        return super(OrderEditView, self).form_valid(form)


class OrderDeleteView(StaffOnlyMixin, generic.DeleteView):
    model = Order
    template_name = 'dashboard/generic_delete.html'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(self.model, uuid=uuid)

    def get_success_url(self):
        messages.info(self.request, 'Order {} deleted'.format(self.object.uuid))
        return reverse('order_panel:order-list')


class OrderDetailView(StaffOnlyMixin, generic.DetailView):
    model = Order
    template_name = 'dashboard/order/order_detail.html'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(self.model, uuid=uuid)


class OrderItemUpdateView(StaffOnlyMixin, generic.UpdateView):
    model = OrderItem
    template_name = 'dashboard/order/order_item_update.html'
    fields = [
        'quantity',
        'price',
    ]

    def get_success_url(self):
        return reverse('order_panel:order-detail', kwargs={'uuid': self.object.order.uuid})


class OrderItemDeleteView(StaffOnlyMixin, generic.DeleteView):
    model = OrderItem
    template_name = 'dashboard/order/order_item_delete.html'

    def get_success_url(self):
        return reverse('order_panel:order-detail', kwargs={'uuid': self.object.order.uuid})

