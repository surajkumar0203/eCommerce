from django.shortcuts import render,redirect

from accounts.models import MyUser as User,Customer,Shopkeeper
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from accounts.utility import create_user_account,login_user_account
from products.models import VendorProducts

# ragister as a custom
def register(request):
    if request.method=="POST":
        data={
            'first_name':request.POST.get('first_name'),
            'last_name':request.POST.get('last_name'),
            'username':request.POST.get('username'),
            'email':request.POST.get('email'),
            'password':request.POST.get('password'),
        }
        response=create_user_account(Customer,**data)
        if "error" in response:
            messages.error(request, response["error"])
            return redirect('/accounts/register/')
        messages.success(request, response["success"])
        return redirect('/')
    
    return render(request, 'register.html')


# ragister as a shopkeeper

def shopkeeper_register(request):
    if request.method=="POST":
        data={
            'first_name':request.POST.get('first_name'),
            'last_name':request.POST.get('last_name'),
            'username':request.POST.get('username'),
            'email':request.POST.get('email'),
            'password':request.POST.get('password'),
            'gst_number':request.POST.get('gstnumber'),
            'aadhar_number':request.POST.get('aadharnumber'),
            'vender_name':request.POST.get('vendername'),
            'bmp_id':request.POST.get('bmpid'),
        }
        try:
            response=create_user_account(Shopkeeper,**data)
            
            if 'error' in response:
                messages.error(request,response['error'])
                return redirect('/accounts/register/')
            
            messages.success(request, response["success"])
        except:
            messages.success(request, 'User already exists')
            return redirect('/')
        
    return render(request, 'register.html')


def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=Customer.objects.filter(username=username).exists()
        if not user_obj:
            messages.error(request,"User Not Found")
            return redirect('/')
        
        if not Customer.objects.get(username=username).is_email_verified:
            messages.error(request,"Email Not Verified")
            return redirect('/')

        user_obj=authenticate(username=username,password=password)
        if user_obj is not None:
            login(request,user_obj)
            messages.success(request,"Login Successfully")
            return redirect('/')
        messages.error(request,"Invalid Credentials")
        return redirect('/')
        
    
    return redirect('/')


def shopkeeper_login(request):
    if request.method=='POST':
       
        username=request.POST.get('username')
        password=request.POST.get('password')
        bmpid=request.POST.get('bmpid')
        try:
            shopkeeper = Shopkeeper.objects.get(username=username,bmp_id=bmpid)
            if not shopkeeper.is_email_verified:
                messages.error(request,"Email Not Verified")
                return redirect('/')
            shopkeeper_obj=authenticate(username=username,password=password)
            if shopkeeper_obj is not None:
                login(request, shopkeeper_obj)
                messages.success(request,"Login Successfully")
                return redirect('/')
            messages.success(request,"Invalid Credentials")
            return redirect('/')

        except Exception as e: 
            messages.success(request,"Invalid Credentials")
            return redirect('/')
    return redirect('/')


@login_required(login_url='/')
def logout_page(request):
    logout(request)
    return redirect('/')


def account_activate(request,token_id): 
    try:
        user_obj=User.objects.get(email_token=token_id)
        if user_obj.is_email_verified:
            messages.success(request,"Your Account is Already Activated")
            return redirect('/')
        
        user_obj.is_email_verified=True
        
        user_obj.save()
        messages.success(request,"Your Account is Activated")
    except Exception as e:
        messages.error(request,"Invalid Token")
        return redirect('/')
    
    return redirect('/')



# user profile
@login_required(login_url='/')
def account_user_profile(request):
    myuser=User.objects.get(username=request.user)
    context={}
   
    
    context['username']=myuser.username
    context['first_name']=myuser.first_name
    context['last_name']=myuser.last_name
    context['email']=myuser.email
    
    if myuser.isShopkeeper:
        shopkeeper=Shopkeeper.objects.get(username=request.user)
        vender_products=VendorProducts.objects.filter(shopkeeper=shopkeeper)
        context['gst_number']=shopkeeper.gst_number
        context['aadhar_number']=shopkeeper.aadhar_number
        context['bmp_id']=shopkeeper.bmp_id
        context['vender_name']=shopkeeper.vender_name
        context['vender_products']=vender_products
    return render(request,'userprofile.html',context)