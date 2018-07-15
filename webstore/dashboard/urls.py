from django.urls import path

from . import views


app_name = 'dashboard'

urlpatterns = [

    path('', views.DashboardWelcomeView.as_view(),
         name='dashboard-main'),

]
