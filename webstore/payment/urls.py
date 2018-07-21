from django.urls import path

from . import views


app_name = 'payment'

urlpatterns = [

    path('user-list/', views.UserOutstandingPaymentsView.as_view(),
         name='user-list'),

]
