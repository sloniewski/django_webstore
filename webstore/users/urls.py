from django.urls import path

from webstore.users import views

app_name = 'users'

urlpatterns = [

    path('login/', views.AuthenticateSession.as_view(), name='login'),

    path('logout/', views.UsersLogoutView.as_view(), name='logout'),

]
