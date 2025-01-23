from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.manager import MyUserManager
from django.core.exceptions import ValidationError
from django.db.models import Count,Q


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
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,blank=True,null=True)

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

    class Meta:
        abstract = True


class Customer(MyUser):
    profile_image= models.ImageField(upload_to="customer/",null=True, blank=True)
    
    
    def getCartItemCount(self):
        from orders.models import CartItem,Carts
        '''
        # Filter object that has customer login and is_paid is false
            Carts.objects.filter(customer=self,is_paid=False)
    
        # Count items that have a login and is_paid=False
        annotate(cart_item_count=Count('cartItem'))

        # sum total which return aggrate
        '''
        
        try:
            # first method using annotate
            cart_items=Carts.objects.filter(customer=self,is_paid=False).annotate(cart_item_count=Count('cartItem')).first()
            # return sum(cart_items)
            
            return cart_items.cart_item_count
            # return sum(cart_item.cart_item_count for cart_item in cart_items)
        except:
            
            return 0
 
        # second method   using filter
        #! return CartItem.objects.filter(customer__customer=self,customer__is_paid=False).count()
        
        
       

class Shopkeeper(MyUser):
    gst_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=14)
    profile_image= models.ImageField(upload_to="shopkeeper/",null=True, blank=True)
    bmp_id = models.CharField(unique=True, max_length=100)
    vender_name = models.CharField(max_length=100)
    
