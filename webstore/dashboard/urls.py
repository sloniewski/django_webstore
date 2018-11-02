from django.urls import path

from . import views


app_name = 'dashboard'

urlpatterns = [

    # Delivery
    path('delivery/list/<status>', views.DeliveryListView.as_view(),
         name='delivery-list'),

    path('delivery/update/<pk>', views.DeliveryUpdateView.as_view(),
         name='delivery-update'),

    # general
    path('', views.DashboardWelcomeView.as_view(),
         name='dashboard-main'),

]
