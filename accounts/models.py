from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.manager import MyUserManager
from django.core.exceptions import ValidationError


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username=models.CharField(max_length=30,blank=False,null=False,unique=True)
    first_name=models.CharField(max_length=150,blank=False,null=False)
    last_name=models.CharField(max_length=150,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
   

    objects = MyUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name","last_name","email"]

   

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def save(self,*args,**kwargs):
        if not(self.first_name and self.last_name and self.email and self.username):
            raise ValueError("All fields are required")
        
        super(MyUser,self).save(*args,**kwargs)



class Customer(MyUser):
    profile_image= models.ImageField(upload_to="customer/",null=True, blank=True)
    
    

class Shopkeeper(MyUser):
    gst_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=14)
    profile_image= models.ImageField(upload_to="shopkeeper/",null=True, blank=True)
    bmp_id = models.CharField(unique=True, max_length=100)
    vender_name = models.CharField(max_length=100)
    

