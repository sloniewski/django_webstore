from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [

    path('add-item/', views.CartAddItem.as_view(),
         name='add-item'),

    path('list-item/', views.CartSummaryView.as_view(),
         name='item-list'),

    path('quick-add-item/item/<int:item_id>', views.CartQuickAddItem.as_view(),
         name='quick-add-item'),

    path('quick-remove-item/item/<int:item_id>', views.CartQuickRemoveItem.as_view(),
         name='quick-remove-item'),
]
