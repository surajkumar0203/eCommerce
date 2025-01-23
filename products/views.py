from django.shortcuts import render
from accounts.models import MyUser as User,Customer,Shopkeeper



def upload_product(request):
    print(request.user)
    print(isinstance(request.user, Shopkeeper))
    return render(request,'products/upload_products.html')
