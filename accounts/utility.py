from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from accounts.models import Shopkeeper

def create_user_account(model, **data):
    """
    Helper function to create a user account.
    - `model`: Model to create the user (Customer or Shopkeeper).
    - `data`: Dictionary of basic user fields.

    """
    
    user_obj=model.objects.filter(Q(username=data['username']) | Q(email=data['email']))

    if user_obj.exists():
        return {"error": "User already exists"}

    try:
        user_obj=model.objects.create(**data)
        user_obj.set_password(data['password'])
        if model==Shopkeeper:
            user_obj.isShopkeeper=True
        user_obj.save()
        return {"success": "Check your email to activate your account"}
    except ValueError as e:
        return {"error": str(e)}


def login_user_account(model,request, **data):
  
    """
    Helper function to login a user account.
    - `model`: Model to authenticate the user (Customer or Shopkeeper).
    - `request`: Django request object.
    """
    users=model.objects.filter(username=data['username'])
    user_obj=users.first()
   
    if not users.exists():
        return {"error": "User Not Found"}
    
    # Additional check for Shopkeeper's BMP ID
    if model == Shopkeeper and user_obj.bmp_id != data.get('bmpid'):
        return {"error": "Invalid BMP ID"}


    if not model.objects.get(username=data['username']).is_email_verified:
        return {"error": "Email Not Verified"}
    user_obj=authenticate(username=data['username'],password=data['password'])
    
    print(user_obj)
    if user_obj is not None:
        login(request,user_obj)
        return {"success": "Login Successfully"}
        
    return {"error": "Invalid Credentials"}