from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Payment, PaymentStatus


class UserOutstandingPaymentsView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payment/user_payment_list.html'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(status__in=PaymentStatus.active())\
            .select_related('order')\
            .filter(order__user=self.request.user)
