from django.http import HttpResponse
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
