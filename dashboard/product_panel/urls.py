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

    path('product/price-list/<int:number>/create', views.ProductPriceCreateView.as_view(),
         name='product-price-create'),

    path('product/price-list/<int:number>', views.ProductPriceListView.as_view(),
         name='product-price-list'),


    path('price/<int:pk>', views.PriceUpdateView.as_view(),
         name='price-update'),

    # Category
    path('category/list', views.CategoryListView.as_view(),
         name='category-list'),

    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(),
         name='category-update'),

    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(),
         name='category-delete'),

    path('category/create/', views.CategoryCreateView.as_view(),
         name='category-create'),

    # Pictures
    path('picture/list/', views.PictureListView.as_view(),
         name='picture-list'),

    path('picture/create/', views.PictureCreateView.as_view(),
         name='picture-create'),

    path('product/<slug:slug>/gallery/', views.GalleryPicturesListView.as_view(),
         name='product-gallery'),

    path('product/<slug:slug>/gallery/upload/', views.GalleryPicturesUploadView.as_view(),
         name='product-gallery-upload'),

]
