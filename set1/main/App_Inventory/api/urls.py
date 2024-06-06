from django.urls import path


from Auth.api.views import (
    CreateUser
)

from App_Inventory.api.views import (
    get_inventory, CreateItem, get_item
)

urlpatterns = [
    path('auth/',CreateUser.as_view(),name='create_user'),
    path('list/',get_inventory,name='get_inventory'),
    path('create-item/',CreateItem.as_view(),name='create_item'),
    path('<int:pk>/',get_item,name='get_item')
]
