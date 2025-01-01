from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from accounts.models import MyUser as User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=username)

        if user_obj.exists():
            messages.error(request,"User Already Exists")
            return redirect('/')
        try:
            user_obj=User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,"Check Your Email To Activate Your Account")
            return redirect('/')
        
        except ValueError as e:
            messages.error(request, str(e)) 
            return redirect('/accounts/register/')
        
   
    return render(request, 'register.html')


def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user_obj=User.objects.filter(username=username).exists()
        if not user_obj:
            messages.error(request,"User Not Found")
            return redirect('/')
        
        if not User.objects.get(username=username).is_email_verified:
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

@login_required(login_url='/')
def logout_page(request):
    logout(request)
    return redirect('/')


def account_activate(request,token_id): 
    try:
        user_obj=User.objects.get(email_token=token_id)
        user_obj.is_email_verified=True
        user_obj.save()
        messages.success(request,"Your Account is Activated")
    except Exception as e:
        messages.error(request,"Invalid Token")
        return redirect('/')
    
    return redirect('/')