from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [

    path('create/', views.OrderCreateView.as_view(),
         name='order-create'),

    path('detail/<int:pk>', views.OrderDetailView.as_view(),
         name='order-detail'),

]
