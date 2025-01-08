from django.contrib import admin
from orders.models import CartItem,Carts


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['customer','product','quantity']

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display=['customer','is_paid']

