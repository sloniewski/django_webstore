import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.defaults import page_not_found, bad_request
from django.views.generic import FormView, ListView

from .forms import AddItemForm, RemoveItemForm
from .models import Cart


class CartQuickRemoveItem(View):

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.modified = True
            request.session.save()
        return super().dispatch(request, args, kwargs)

    def post(self, request, *args, **kwawrgs):
        item_id = request.resolver_match.kwargs['item_id']
        cart = Cart.objects.get_or_create(
            session=self.request.session.session_key)[0]
        item = cart.remove_item(item=item_id, qty=1)

        if item is None:
            return HttpResponse(status=204)

        data = {
            'cart_items': cart.item_count,
            'cart_value': cart.value,
            'item_qty': item.quantity,
            'item_value': item.item_value,
        }
        return JsonResponse(data=data, status=200)


class CartQuickAddItem(View):

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
            'item_value': item.item_value,
            }
        return JsonResponse(data=data)


class CartAddItem(FormView):
    form_class = AddItemForm

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
            'cart_items': cart.get_item_count(),
        })
        return HttpResponse(data)

    def form_invalid(self, form):
        return bad_request(self.request, 'bad request')


class CartRemoveItem(FormView):
    form_class = RemoveItemForm

    def get(self, request, *args, **kwargs):
        return page_not_found(request, 'page not found')

    def form_valid(self, form):

        cart = Cart.objects.get(session=self.request.session.session_key)
        # TODO view not finished

    def form_invalid(self, form):
        return bad_request(self.request, 'bad request')


class CartListView(ListView):
    template_name = 'cart/cart_list.html'

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
