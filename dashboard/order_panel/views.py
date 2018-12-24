from django.views import generic
from django.shortcuts import reverse, get_object_or_404
from django.db.models import Count
from django.contrib import messages

from django_filters.views import FilterView

from webstore.order.models import Order, OrderItem
from .forms import FilterOrdersForm, OrderUpdateForm


class OrderListView(FilterView):
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


class OrderUpdateView(generic.UpdateView):
    model = Order
    template_name = 'dashboard/order/order_update.html'
    form_class = OrderUpdateForm

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(self.model, uuid=uuid)


class OrderDeleteView(generic.DeleteView):
    model = Order
    template_name = 'dashboard/generic_delete.html'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(self.model, uuid=uuid)

    def get_success_url(self):
        messages.info(self.request, 'Order {} deleted'.format(self.object.uuid))
        return reverse('order_panel:order-list')


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'dashboard/order/order_detail.html'


class OrderItemUpdateView(generic.UpdateView):
    model = OrderItem
    template_name = 'dashboard/order/order_item_update.html'
    fields = [
        'quantity',
        'price',
    ]

    def get_success_url(self):
        return reverse('dashboard:order-detail', kwargs={'pk': self.object.order.id})


class OrderItemDeleteView(generic.DeleteView):
    model = OrderItem
    template_name = 'dashboard/order/order_item_delete.html'

    def get_success_url(self):
        return reverse('dashboard:order-detail', kwargs={'pk': self.object.order.id})

