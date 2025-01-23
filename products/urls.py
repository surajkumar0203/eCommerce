from django.urls import path
from products.views import upload_product


urlpatterns = [
   path('upload/',upload_product,name="upload_product")
]