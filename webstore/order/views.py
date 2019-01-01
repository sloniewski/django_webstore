from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, reverse
from django.views.generic import DetailView, FormView, ListView

from webstore.cart.models import Cart
from webstore.delivery.forms import ChooseDeliveryForm
from webstore.delivery.models import Delivery
from webstore.payment.models import Payment

from .models import Order, OrderItem


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'webstore/order/order_detail.html'
    pk_url_kwarg = 'uuid'
    http_method_names = ['get', 'head', 'options']

    def get_object(self, queryset=None):
        uuid = self.kwargs.get(self.pk_url_kwarg)
        object = self.model.objects\
            .filter(uuid=uuid)\
            .select_related('delivery')\
            .prefetch_related('orderitems')\
            .first()
        return object


class OrderConfirmView(LoginRequiredMixin, FormView):
    """ view that removes cart and creates order in place """

    form_class = ChooseDeliveryForm
    template_name = 'webstore/order/order_add_delivery.html'
    cart = None

    def get_login_url(self):
        return reverse('users:login')

    def handle_no_permission(self):
        return redirect('users:login')

    def form_valid(self, form):
        # TODO bug - you can create an order with no items
        order = Order.objects.create_from_cart(
            cart=self.get_cart(),
            user=self.request.user
            )
        # create from cart sets status for order
        delivery = form.save(commit=False)
        delivery.order = order
        delivery.save()

        Payment.objects.create_for_order(
            order=order,
            delivery=delivery,
        )
        mail = order.get_status_mail()
        mail.send(fail_silently=False)

        return redirect('order:order-summary', uuid=order.uuid)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['cart'] = self.get_cart()
        return kwargs

    def get_initial(self):
        last_delivery = Delivery.objects.get_last(self.request.user)
        if last_delivery is None:
            return {}
        return dict(last_delivery)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cart_item_count': self.get_cart().item_count,
            'cart_value': self.get_cart().value,
            'cart_items_list': self.get_cart().get_items(),
        })
        return context

    def get_cart(self):
        if self.cart is None:
            self.cart = Cart.objects.recive_or_create(self.request)
        return self.cart


class OrderSummary(LoginRequiredMixin, ListView):
    template_name = 'webstore/order/order_summary.html'
    model = OrderItem
    pk_url_kwarg = 'uuid'

    def get(self, request, *args, **kwargs):
        order_id = request.resolver_match.kwargs[self.pk_url_kwarg]
        self.order = get_object_or_404(Order, uuid=order_id)
        if request.user != self.order.user:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(order=self.order)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'webstore/order/order_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).with_properties()
