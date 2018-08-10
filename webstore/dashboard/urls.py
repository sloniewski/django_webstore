from django.urls import path

from . import views


app_name = 'dashboard'

urlpatterns = [

    path('product/list', views.ProductListView.as_view(),
         name='product-list'),

    path('product/update/<int:pk>', views.ProductUpdateView.as_view(),
         name='product-update'),

    path('product/delete/<int:pk>', views.ProductDeleteView.as_view(),
         name='product-delete'),

    path('product/price-list/<int:pk>', views.ProductPriceListView.as_view(),
         name='product-price-list'),

    path('product/create', views.ProductCreateView.as_view(),
         name='product-create'),


    path('order/<pk>', views.OrderDetailView.as_view(),
         name='order-detail'),

    path('order/list/<status>', views.OrderListView.as_view(),
         name='order-list'),

    path('order/update/<pk>', views.OrderUpdateView.as_view(),
         name='order-update'),


    path('payment/list/<status>', views.PaymentListView.as_view(),
         name='payment-list'),

    path('payment/update/<pk>', views.PaymentUpdateView.as_view(),
         name='payment-update'),


    path('delivery/list/<status>', views.DeliveryListView.as_view(),
         name='delivery-list'),

    path('delivery/update/<pk>', views.DeliveryUpdateView.as_view(),
         name='delivery-update'),


    path('', views.DashboardWelcomeView.as_view(),
        name='dashboard-main'),

]
