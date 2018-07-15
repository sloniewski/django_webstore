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

    path('', views.DashboardWelcomeView.as_view(),
             name='dashboard-main'),

]
