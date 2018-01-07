from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [

    path('add-item/', views.CartAddItem.as_view(),
         name='add-item'),

]
