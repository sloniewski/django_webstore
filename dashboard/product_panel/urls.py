from django.urls import path

from . import views


app_name = 'product_panel'

urlpatterns = [

    # Product
    path('list', views.ProductListView.as_view(),
         name='product-list'),

    path('update/<slug>', views.ProductUpdateView.as_view(),
         name='product-update'),

    path('delete/<slug>', views.ProductDeleteView.as_view(),
         name='product-delete'),

    path('create', views.ProductCreateView.as_view(),
         name='product-create'),

    path('product/price-list/<int:number>', views.ProductPriceListView.as_view(),
         name='product-price-list'),

]
