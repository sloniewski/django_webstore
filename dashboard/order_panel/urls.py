from django.urls import path

from . import views


app_name = 'order_panel'

urlpatterns = [
    
    # Order
    path('list', views.OrderListView.as_view(),
         name='order-list'),

    path('<uuid>', views.OrderDetailView.as_view(),
         name='order-detail'),

    path('<uuid>/delete', views.OrderDeleteView.as_view(),
         name='order-delete'),

    path('<uuid>/update', views.OrderUpdateView.as_view(),
         name='order-update'),

     path('<uuid>/edit', views.OrderEditView.as_view(),
          name='order-edit'),

    # OrderItem
    path('update/item/<pk>', views.OrderItemUpdateView.as_view(),
         name='order-item-update'),

    path('delete/item/<pk>', views.OrderItemDeleteView.as_view(),
         name='order-item-delete'),

]
