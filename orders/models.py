from django.db import models
from accounts.models import Customer,MyUser
from products.models import VendorProducts
from django.db.models import Sum,F




class Carts(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="customer_cart")
    is_paid=models.BooleanField(default=False)
    order_id=models.CharField(max_length=200,null=True,blank=True)
    payment_id=models.CharField(max_length=2000,null=True,blank=True)
    payment_signature=models.CharField(max_length=5000,null=True,blank=True)
    
    def calculate_delivery_fee(self):
        delivery_fee=self.cartItem.aggregate(
            d_fee=Sum('product__delivery_price')
        )['d_fee']
        
        return delivery_fee or 0
    
    def tax(self):
        return 50
    
    # F when calculate on sport calculate during fetching data
    def get_cart_total_price(self):
        total_amount=self.cartItem.aggregate(
           
            total=Sum(F('product__vendor_selling_price')*F('quantity'))
        )['total']
        return total_amount or 0
        
    
    def final_price(self):
        total_price=self.get_cart_total_price()
        delivery_fee=self.calculate_delivery_fee()
        tax=self.tax()
        final_price=total_price+delivery_fee+tax
        return final_price

class CartItem(models.Model):
    customer=models.ForeignKey(Carts,on_delete=models.CASCADE,related_name="cartItem")
    product=models.ForeignKey(VendorProducts,null=True,on_delete=models.SET_NULL,related_name="product_item")
    quantity=models.IntegerField(default=0)
    
    def cart_total_price(self):
        selling_price=self.product.vendor_selling_price
        selling_price*=self.quantity
        return selling_price