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

    path('category/list', views.CategoryListView.as_view(),
         name='category-list'),

    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(),
         name='category-update'),

    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(),
         name='category-delete'),

    path('category/create/', views.CategoryCreateView.as_view(),
         name='category-create'),

]
