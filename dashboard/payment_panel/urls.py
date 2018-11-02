from django.urls import path

from . import views


app_name = 'payment_panel'

urlpatterns = [

    # Payment
    path('list/<status>', views.PaymentListView.as_view(),
         name='payment-list'),

    path('update/<pk>', views.PaymentUpdateView.as_view(),
         name='payment-update'),

]