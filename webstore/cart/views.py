import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.defaults import page_not_found, bad_request
from django.views.generic import FormView, ListView

from webstore.core.mixins import ForceSessionMixin

from .forms import ItemForm
from .models import Cart, CartItem


class CartMixin:

    def get_cart(self, request):
        cart = Cart.objects.get_or_create(
            session=request.session.session_key,
        )[0]
        return cart


class CartQuickRemoveItem(CartMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwawrgs):
        item_id = request.resolver_match.kwargs['item_id']
        cart = self.get_cart(self.request)
        item = cart.remove_item(item=item_id, qty=1)

        if item is None:
            return HttpResponse(status=204)

        data = {
            'cart_items': cart.item_count,
            'cart_value': cart.value,
            'item_qty': item.quantity,
            'item_value': item.value,
        }
        return JsonResponse(data=data, status=200)


class CartQuickAddItem(CartMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        item_id = request.resolver_match.kwargs['item_id']
        cart = self.get_cart(self.request)
        item = cart.add_item(item_id, 1)
        data = {
            'cart_items': cart.item_count,
            'cart_value': cart.value,
            'item_qty': item.quantity,
            'item_value': item.value,
            }
        return JsonResponse(data=data, status=201)


class CartQuickDeleteItem(CartMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwawrgs):
        cart = self.get_cart(self.request)
        item_id = request.resolver_match.kwargs.get('item_id')
        cart.delete_item(item_id)
        data = {
            'cart_items': cart.item_count,
            'cart_value': cart.value,
            }
        return JsonResponse(data=data, status=200)


class CartAddItem(CartMixin, FormView):
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        return page_not_found(request, 'page not found')

    def form_valid(self, form):
        item = form.cleaned_data['item']
        qty = form.cleaned_data['qty']
        cart = self.get_cart(self.request)
        cart.add_item(item, qty)

        data = json.dumps({
            'added': {
                'item': item,
                'qty': qty,
            },
            'cart_items': cart.item_count,
        })
        return HttpResponse(data)

    def form_invalid(self, form):
        return bad_request(self.request, 'bad request')


class CartListView(ForceSessionMixin, ListView):
    template_name = 'webstore/cart/cart_list.html'
    model = CartItem

    def get_queryset(self):
        queryset = CartItem.objects\
            .filter(cart__session=self.request.session.session_key)\
            .select_related('product')
        return queryset
    
    def get_context_data(self):
        context = super().get_context_data()
        cart = Cart.objects.get_or_create(
            session=self.request.session.session_key,
        )[0]
        context.update({
                'cart_value': cart.value,
                'cart_item_count': cart.item_count,
            })
        return context

