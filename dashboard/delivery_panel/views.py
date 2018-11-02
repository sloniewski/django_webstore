from django.views import generic

from django_filters.views import FilterView

from webstore.delivery.models import Delivery
from webstore.order.models import Order

from .forms import DeliveryUpdateForm, FilterDelieriesForm


class DeliveryListView(FilterView):
    model = Delivery
    template_name = 'dashboard/delivery/delivery_list.html'
    filterset_class = FilterDelieriesForm
    strict = False


class DeliveryUpdateView(generic.UpdateView):
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

