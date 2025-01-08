from django.shortcuts import render
from orders.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import VendorProducts,Products
from django.contrib import messages
from accounts.models import MyUser,Customer

@login_required(login_url='/accounts/login/')
def add_to_cart(request):
    try:
        current_customer = request.user
       
        my_user=Customer.objects.get(username=current_customer)
        
        product_id = request.GET.get('product_id')
    
        vendor_products = VendorProducts.objects.get(product=product_id)
      
        cart,_=Carts.objects.get_or_create(customer=my_user)
        cart_item,_=CartItem.objects.get_or_create(customer=cart,product=vendor_products)
        cart_item.quantity+=1
        cart_item.save()
        
    except Exception as e:
        
        messages.success(request,"Invailid Product id")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    messages.success(request,"Item added successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/accounts/login/')
def remove_to_cart(request):
    try:
        current_customer = request.user
       
        my_user=Customer.objects.get(username=current_customer)
       
        product_id = request.GET.get('product_id')
    
        vendor_products = VendorProducts.objects.get(product=product_id)
        
        cart,_=Carts.objects.get_or_create(customer=my_user)
        cart_item,_=CartItem.objects.get_or_create(customer=cart,product=vendor_products)
        cart_item.quantity-=1
        cart_item.save()
        if cart_item.quantity<=1:
            cart_item.delete()
        
    except Exception as e:
        messages.success(request,"Invailid Product id")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    messages.success(request,"Item removed successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

