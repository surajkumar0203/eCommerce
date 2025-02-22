from django.db import models
from accounts.models import Customer,MyUser
from products.models import VendorProducts
from django.db.models import Sum,F
from utils.utility import generate_order_id,generate_slug,generate_order_pdf
from datetime import date


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

    def cart_to_order(self):
        order=Order.objects.create(
            customer=self.customer,
            cart_item=self,
            payment_id=self.payment_id,
            payment_signature=self.payment_signature,
            final_price=self.final_price()
        )
        
        for cart_item in self.cartItem.all():
            
            OrderItem.objects.create(
                product=cart_item.product,
                order=order,
                slug=generate_slug(order_id=order.order_id),
                quantity=cart_item.quantity,
                per_product_price=cart_item.product.vendor_selling_price,
                total_price=cart_item.product.vendor_selling_price*cart_item.quantity
            )

    
class CartItem(models.Model):
    customer=models.ForeignKey(Carts,on_delete=models.CASCADE,related_name="cartItem")
    product=models.ForeignKey(VendorProducts,null=True,on_delete=models.SET_NULL,related_name="product_item")
    quantity=models.IntegerField(default=0)
    
    def cart_total_price(self):
        selling_price=self.product.vendor_selling_price
        selling_price*=self.quantity
        return selling_price


class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="customer_order")
    cart_item=models.ForeignKey(Carts,on_delete=models.CASCADE,related_name="cart_item_order")
    order_id=models.CharField(max_length=200,null=True,blank=True)
    payment_id=models.CharField(max_length=2000,null=True,blank=True)
    payment_signature=models.CharField(max_length=5000,null=True,blank=True)
    final_price=models.FloatField()

    def __str__(self):
        return str(self.order_id)
    
    def save(self, *args, **kwargs):
        self.order_id=generate_order_id(Order.objects.count())
        super(Order,self).save(*args, **kwargs)
        
       
        

    def get_order_data(self):
        
        order_data={
           'invoice':{
                'invoice_number':self.order_orderItem.all().first().slug,
                'date':date.today(),
           },
           
           'customer':{
                'Customer_name':self.customer.first_name+" "+self.customer.last_name,
                'Customer_email':self.customer.email,
            },
            'shop_keeper':{
                "seller_name":self.order_orderItem.all().first().product.shopkeeper.first_name+" "+self.order_orderItem.all().first().product.shopkeeper.last_name,
                'sheller_email':self.order_orderItem.all().first().product.shopkeeper.email
            },
           
            'order':{
                'order_id':self.order_id,
                'final_price':self.final_price,
                'delivery_price':self.order_orderItem.all().first().product.delivery_price,
                'tax':self.cart_item.tax()
            },
        
           'order_items': [ 
                {
                    'product_name':order_item.product.product.item_name,
                    'Quantity':order_item.quantity,
                    'per_price':order_item.per_product_price,
                    'total':order_item.total_price,
                
                } for order_item in self.order_orderItem.all()
            ]
        }

        return order_data

class OrderItem(models.Model):
    order_choice=(
        ("Order Received","Order Received"),
        ("Order Packed","Order Packed"),
        ("Order Shipped","Order Shipped"),
        ("Out Of Delivery","Out Of Delivery"),
        ("Order Delivered","Order Delivered"),
    )
    product=models.ForeignKey(VendorProducts,null=True,on_delete=models.SET_NULL,related_name="product_OrderItem")
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_orderItem")
    quantity=models.IntegerField(default=0)
    per_product_price=models.FloatField()
    total_price=models.FloatField()
    slug=models.SlugField(unique=True)
    status=models.CharField(max_length=150,choices=order_choice,default="Order Received")
    def __str__(self):
        return str(self.order.order_id)
    
    