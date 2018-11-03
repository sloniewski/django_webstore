import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.defaults import page_not_found, bad_request
from django.views.generic import FormView, ListView

from .forms import ItemForm
from .models import Cart


class CartQuickRemoveItem(View):
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.modified = True
            request.session.save()
        return super().dispatch(request, args, kwargs)

    def post(self, request, *args, **kwawrgs):
        item_id = request.resolver_match.kwargs['item_id']
        cart = Cart.objects.recive_or_create(self.request)
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


class CartQuickAddItem(View):
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.modified = True
            request.session.save()
        return super().dispatch(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        item_id = request.resolver_match.kwargs['item_id']
        cart = Cart.objects.recive_or_create(self.request)
        item = cart.add_item(item_id, 1)
        data = {
            'cart_items': cart.item_count,
            'cart_value': cart.value,
            'item_qty': item.quantity,
            'item_value': item.value,
            }
        return JsonResponse(data=data)


class CartDeleteItem(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        item_id = request.resolver_match.kwargs['item_id']
        cart = Cart.objects.recive_or_create(self.request)
        item = cart.cartitem_set.filter(pk=item_id)
        item.delete()
        data = {
            'cart_items': cart.item_count,
            'cart_value': cart.value,
            }
        return JsonResponse(data=data)


class CartAddItem(FormView):
    form_class = ItemForm

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.modified = True
            request.session.save()
        return super().dispatch(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        return page_not_found(request, 'page not found')

    def form_valid(self, form):

        item = form.cleaned_data['item']
        qty = form.cleaned_data['qty']
        cart = Cart.objects.recive_or_create(self.request)
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


class CartListView(ListView):
    template_name = 'webstore/cart/cart_list.html'

    def get_queryset(self):
        try:
            cart = Cart.objects.get(session=self.request.session.session_key)
            self.extra_context = {
                'cart_value': cart.value,
                'cart_item_count': cart.item_count,
            }
        except Cart.DoesNotExist:
            return None
        return cart.get_items()
