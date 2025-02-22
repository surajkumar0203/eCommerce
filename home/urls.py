from django.urls import path,include
from home.views import home,product_details

urlpatterns = [
    path('', home,name='home'),
    path('product-details/<product_sku>/', product_details,name='product_details'),
]