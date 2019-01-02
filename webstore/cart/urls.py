from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [

    path('add-item/', views.CartAddItem.as_view(),
         name='add-item'),

    path('list-item/', views.CartListView.as_view(),
         name='item-list'),

    path('item/add/<int:item_id>', views.CartQuickAddItem.as_view(),
         name='quick-add-item'),

    path('item/remove/<int:item_id>', views.CartQuickRemoveItem.as_view(),
         name='quick-remove-item'),

    path('item/delete/<int:item_id>', views.CartQuickDeleteItem.as_view(),
         name='quick-delete-item'),

]
