import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.defaults import page_not_found, bad_request
from django.views.generic import FormView, ListView

from .forms import AddItemForm, RemoveItemForm
from .models import Cart


class CartQuickAddItem(View):

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.modified = True
            request.session.save()
        return super().dispatch(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        item_id = request.resolver_match.kwargs['item_id']
        cart = Cart.objects.get_or_create(session_id=self.request.session.session_key)[0]
        cart.add_item(item_id, 1)
        return JsonResponse(data={'cart_items': cart.get_item_count()})


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
        cart = Cart.objects.get_or_create(session_id=self.request.session.session_key)[0]
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

        cart = Cart.objects.get(session_id=self.request.session.session_key)
        # TODO view not finished

    def form_invalid(self, form):
        return bad_request(self.request, 'bad request')


class CartSummaryView(ListView):
    template_name='cart/cart_list.html'

    def get_queryset(self):
        try:
            cart = Cart.objects.get(session_id=self.request.session.session_key)
        except Cart.DoesNotExist:
            return None
        return cart.get_items()
