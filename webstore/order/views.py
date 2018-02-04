from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView

from webstore.cart.models import Cart

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