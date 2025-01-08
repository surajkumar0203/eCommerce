from django.db import models
from accounts.models import Customer,MyUser
from products.models import VendorProducts





class Carts(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="customer_cart")
    is_paid=models.BooleanField(default=False)


class CartItem(models.Model):
    customer=models.ForeignKey(Carts,on_delete=models.CASCADE,related_name="cartItem")
    product=models.ForeignKey(VendorProducts,null=True,on_delete=models.SET_NULL,related_name="product_item")
    quantity=models.IntegerField(default=0)
    
