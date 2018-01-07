from django.http import JsonResponse, HttpResponse
from django.views.defaults import page_not_found, bad_request
from django.views.generic import FormView

from .forms import AddItemForm
from .models import Cart

import json


class CartAddItem(FormView):
    form_class = AddItemForm

    def get(self, request, *args, **kwargs):
        return page_not_found(request, 'page not found')

    def form_valid(self, form):

        if self.request.session.session_key is None:
            self.request.session.modified = True
            self.request.session.save()

        item = form.cleaned_data['item']
        qty = form.cleaned_data['qty']

        cart = Cart.objects.get_or_create(self.request.session.session_key)
        cart.add_item(item, qty)

        return HttpResponse(
                    json.loads({ 'item': item,
                                 'qty': qty,
                                 'cart_items': cart.items,
                                 }
                               )
        )

    def form_invalid(self, form):
        return bad_request(self.request, 'bad request')
