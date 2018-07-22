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


    path('payment/list/<status>', views.PaymentListView.as_view(),
         name='payment-list'),

    path('payment/update/<pk>', views.PaymentUpdateView.as_view(),
         name='payment-update'),


    path('', views.DashboardWelcomeView.as_view(),
             name='dashboard-main'),

]
