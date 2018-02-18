from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [

    path('create/', views.OrderCreateView.as_view(),
         name='order-create'),
        
    path('list/', views.OrderListView.as_view(),
         name='order-list'),

    path('detail/<int:pk>', views.OrderDetailView.as_view(),
         name='order-detail'),

    path('confirm/<int:pk>', views.OrderAddDeliveryView.as_view(),
         name='order-confirm'),

    path('payment/<int:pk>', views.OrderAddPaymentView.as_view(),
         name='order-payment'),

]
