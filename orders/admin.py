from django.contrib import admin
from orders.models import CartItem,Carts,Order,OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['customer','product','quantity']

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display=['customer','is_paid']
    readonly_fields=['order_id','payment_id','payment_signature']

admin.site.register(Order)
admin.site.register(OrderItem)