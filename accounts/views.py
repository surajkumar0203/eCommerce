from django.shortcuts import render,redirect
from django.contrib.auth.models import User
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

        user_obj=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request,"User Created Successfully")
        return redirect('/')
   
    return render(request, 'register.html')


def login_page(request):
    print("Login")
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user_obj=User.objects.filter(username=username).exists()
        if not user_obj:
            messages.error(request,"User Not Found")
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