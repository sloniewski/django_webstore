from django.urls import path

from webstore.users import views

app_name = 'users'

urlpatterns = [

    path('users/', views.UsersLoginView.as_view(),
         name='login'),

]
