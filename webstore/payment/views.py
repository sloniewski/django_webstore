from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Payment
from webstore.order.models import OrderStatus


class UserOutstandingPaymentsView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'webstore/payment/user_payment_list.html'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(order__status=OrderStatus.AWAITING_PAYMENT.name)\
            .select_related('order')\
            .filter(order__user=self.request.user)
