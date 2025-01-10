from django.urls import path
from orders.views import add_to_cart,remove_to_cart,get_cart,success_page

urlpatterns = [
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('remove_to_cart/',remove_to_cart,name='remove_to_cart'),
    path('cart/',get_cart,name='get_cart'),
    path('success/',success_page,name='success_page'),
]