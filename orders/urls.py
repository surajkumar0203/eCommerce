from django.urls import path
from orders.views import add_to_cart,remove_to_cart

urlpatterns = [
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('remove_to_cart/',remove_to_cart,name='remove_to_cart')
]