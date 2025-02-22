from django.urls import path
from orders.views import add_to_cart,remove_to_cart,get_cart,success_page,myorder,track_order,invoice,downloadPdf

urlpatterns = [
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('invoice/',invoice,name='invoice'),
    path('download_invoice/',downloadPdf,name='download_invoice'),
    path('remove_to_cart/',remove_to_cart,name='remove_to_cart'),
    path('cart/',get_cart,name='get_cart'),
    path('success/',success_page,name='success_page'),
    path('myorder/',myorder,name='myorder'),
    path('track',track_order,name='track_order'),
]