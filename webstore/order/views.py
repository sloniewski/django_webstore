from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, FormView, ListView, UpdateView

from webstore.payment.forms import ChoosePaymentForm
from webstore.cart.models import Cart
from webstore.delivery.forms import ChooseDeliveryForm


from .models import Order


class OrderCreateView(View):

    def get(self, request):

        cart = Cart.objects.get(session_id=request.session.session_key)
        order = Order.objects.create_from_cart(cart=cart, user=request.user)
        cart.delete()

        return redirect('order:order-detail', kwargs={'pk': order.id})


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'


class OrderAddDeliveryView(FormView):
    form_class = ChooseDeliveryForm
    template_name = 'order/order_add_delivery.html'

    def dispatch(self, request, *args, **kwargs):
        order_id = request.resolver_match.kwargs['pk']
        self.order = get_object_or_404(Order, pk=order_id)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['order'] = self.order
        return kwargs

    def form_valid(self, form):
        form.add_delivery()
        return redirect('order:order-payment')


class OrderAddPaymentView(FormView):
    form_class = ChoosePaymentForm
    template_name = 'order/order_add_payment.html'

    def dispatch(self, request, *args, **kwargs):
        order_id = request.resolver_match.kwargs['pk']
        self.order = get_object_or_404(Order, pk=order_id)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['order'] = self.order
        return kwargs

    def form_valid(self, form):
        form.add_payment()
        self.order.status = self.order.CONFIRMED
        self.order.save()
        return redirect('order:order-list')


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
