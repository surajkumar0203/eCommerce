from django.shortcuts import render,redirect
from orders.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import VendorProducts,Products
from django.contrib import messages
from accounts.models import MyUser,Customer
from django.views.decorators.csrf import csrf_exempt
from orders.payments import RazorPayPayment
import json
from orders.tasks import send_Email
from utils.utility import generate_order_pdf
from utils.utility import is_shopkeeper



@login_required(login_url='/accounts/login/')
def add_to_cart(request):
    try:
        current_customer = request.user
       
        my_user=Customer.objects.get(username=current_customer)
        print(my_user)
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
        
        quantity=request.GET.get('quantity')
       
        cart,_=Carts.objects.get_or_create(customer=my_user)
        cart_item,_=CartItem.objects.get_or_create(customer=cart,product=vendor_products)
        if(quantity):
           cart_item.quantity-=int(quantity)
        else:
            cart_item.quantity-=1
        cart_item.save()
        if cart_item.quantity<=0:
            cart_item.delete()
        
    except Exception as e:
        messages.success(request,"Invailid Product id")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    messages.success(request,"Item removed successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login/')
@is_shopkeeper("customer")
def get_cart(request):
    try:
        current_customer = request.user
        
        my_user=Customer.objects.get(username=current_customer)
        cart=Carts.objects.get(customer=my_user)
        cart_items=CartItem.objects.filter(customer=cart).order_by('product')
        
        # payment_process
        name = f"{my_user.first_name} {my_user.last_name}"
        amount=cart.final_price()
        payment=RazorPayPayment("INR")
        payment_info=payment.process_payment(amount=amount,receipt_name=name)
        cart.order_id=payment_info['id']
        cart.save()
        
        context={
            'cart_items':cart_items,
            'cart':cart,
            'payment_info':payment_info,
            
        }
        return render(request,'order/cart.html',context)
    except Exception as e:
       
        pass
    return render(request,'order/cart.html')

@csrf_exempt
def success_page(request):
    razor_pay_ref=request.POST
    
    try:
        if request.method == "POST":
            payment_id=razor_pay_ref["razorpay_payment_id"]
            order_id=razor_pay_ref['razorpay_order_id']
            payment_signature=razor_pay_ref['razorpay_signature']
            
    
            cart=Carts.objects.get(order_id=order_id)
            cart.payment_id=payment_id
            
            cart.payment_signature=payment_signature
            amount=cart.final_price()
            cart.save()
            cart.cart_to_order()
            
            cart_item=CartItem.objects.filter(customer=cart)
            cart_item.delete()
            
            context={
                "order_id":order_id,
                "amount":amount
            }
            return render(request,'order/success_payment.html',context)
    except:
        
        order_id=json.loads(razor_pay_ref['error[metadata]'])
        description=razor_pay_ref['error[description]']
        order_id=order_id['order_id']
        
        cart=Carts.objects.get(order_id=order_id)
        amount=cart.final_price()
        context={
            "order_id":order_id,
            "description":description,
            "amount":amount
        }
        return render(request,'order/fail_payment.html',context)
    return redirect("/")

@login_required(login_url='/accounts/login/')
def myorder(request):
    
    order_items=OrderItem.objects.filter(order__customer=request.user).order_by('-slug')
    
    context={
        'order_items':order_items
    }
    return render(request,'order/myorder.html',context)

@login_required(login_url='/accounts/login/')
def track_order(request):
    
    track_id=request.GET.get('track_id')
    try:
        order_item=OrderItem.objects.get(slug=track_id)
        context={
            'order_item':order_item
        }
        return render(request,'order/track.html',context)
    except:
        pass
    return redirect("/")


def invoice(request):
    order=Order.objects.filter(customer=request.user)
    return render(request,'order/invoicelist.html',{'orders':order})



@login_required(login_url='/accounts/login/')
def downloadPdf(request):
    try:
        order_id=request.GET.get('orderid')
        orders=Order.objects.filter(customer=request.user,order_id=order_id)
        
        if orders.exists():
            generate_order_pdf(orders.first())
            send_Email.delay(order_id,request.user.email)
        else:
            return redirect('/orders/invoice/')
            
    except Exception as e:
        pass
    return redirect('/orders/invoice/')