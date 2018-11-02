from django.views import generic
from django.shortcuts import reverse

from django_filters.views import FilterView

from webstore.order.models import Order, OrderItem, OrderStatus
from .forms import FilterOrdersForm


class OrderListView(FilterView):
    model = Order
    template_name = 'dashboard/order/order_list.html'
    filterset_class = FilterOrdersForm
    strict = False


class OrderUpdateView(generic.View):
    template_name = 'dashboard/order/order_update.html'


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

