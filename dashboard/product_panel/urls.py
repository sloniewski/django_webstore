from django.urls import path

from . import views


app_name = 'product_panel'

urlpatterns = [

    # Product
    path('/list', views.ProductListView.as_view(),
         name='product-list'),

]
