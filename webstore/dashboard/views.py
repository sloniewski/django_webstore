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
from webstore.order.models import Order, OrderItem, OrderStatus

from .forms import (
    AddProductForm,
    FilterDelieriesForm,
    FilterPaymentsForm,
    FilterOrdersForm,
    UpdatePaymentForm,
    DeliveryUpdateForm,
)


class DashboardWelcomeView(TemplateView):
    """
    Generic TemplateView,
    **Template:**
    :template:`dasboard/base_dashboard.html`
    """
    template_name = 'dashboard/base_dashboard.html'


class ProductCreateView(CreateView):
    template_name = 'dashboard/product/product_create.html'
    form_class = AddProductForm

    def get_success_url(self):
        return reverse('dashboard:product-list')


class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/product/product_list.html'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'dashboard/product/product_update.html'
    fields = [
        'name',
        'active',
        'slug',
        'description',
        'weight',
    ]


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'dashboard/product/product_delete.html'


class ProductPriceListView(ListView):
    model = Price
    template_name = 'dashboard/product/product_price_list.html'

    def get_queryset(self):
        number = self.request.resolver_match.kwargs['number']
        product = get_object_or_404(Product, number=number)
        self.update_context({'product': product})
        return Price.objects.filter(product=product)

    def update_context(self, data_dict):
        if self.extra_context is None:
            self.extra_context = data_dict
        else:
            self.extra_context.update(data_dict)


class PaymentListView(FilterView):
    model = Payment
    template_name = 'dashboard/payment/payment_list.html'
    filter_form_class = FilterPaymentsForm

    def get_queryset(self, *args, **kwargs):
        status = self.request.resolver_match.kwargs.get('status').upper()
        status = PaymentStatus[status].name
        if status is not None:
            queryset = super().get_queryset(*args, **kwargs)
            queryset = queryset.filter(status=status)
            return queryset
        else:
            return super().get_queryset(*args, **kwargs)


class PaymentUpdateView(UpdateView):
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


class OrderListView(FilterView):
    model = Order
    template_name = 'dashboard/order/order_list.html'
    filter_form_class = FilterOrdersForm

    def get_queryset(self, *args, **kwargs):
        status = self.request.resolver_match.kwargs.get('status').upper()
        status = OrderStatus[status].name
        if status is not None:
            queryset = super().get_queryset(*args, **kwargs)
            queryset = queryset.filter(status=status)
            return queryset
        else:
            return super().get_queryset(*args, **kwargs)


class OrderUpdateView(View):
    template_name = 'dashboard/order/order_update.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'dashboard/order/order_detail.html'


class OrderItemUpdateView(UpdateView):
    model = OrderItem
    template_name = 'dashboard/order/order_item_update.html'
    fields = [
        'quantity',
        'price',
    ]

    def get_success_url(self):
        return reverse('dashboard:order-detail', kwargs={'pk': self.object.order.id})


class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = 'dashboard/order/order_item_delete.html'

    def get_success_url(self):
        return reverse('dashboard:order-detail', kwargs={'pk': self.object.order.id})
