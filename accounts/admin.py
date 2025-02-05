from django.contrib import admin
from accounts.models import MyUser,Shopkeeper,Customer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin




@admin.register(Shopkeeper)
class ShopkeeperAdmin(BaseUserAdmin):
    list_display = ["id","username","first_name","last_name","email","vender_name"]
    list_filter = ["email"]
    
    fieldsets = [
        ("User Credentials", {"fields": ["username","email", "password"]}),
        ("Personal info", {"fields": ["first_name","last_name","email_token"]}),
        ("Shop Info", {"fields": ["gst_number","aadhar_number","bmp_id","vender_name"]}),
        ("Permissions", {"fields": ["is_active","is_staff","is_email_verified","isShopkeeper"]}),
    ]
    
    add_fieldsets = [
        (
            "User Credentials",
            {
                "classes": ["wide"],
                "fields": ["username","email", "password1", "password2"],
            },
           
            
        ),
        (
             "Personal info",
            {
                "classes": ["wide"],
                "fields": ["first_name","last_name","profile_image"],
            },
        ),
        (
             "Shop Info",
            {
                "classes": ["wide"],
                "fields": ["gst_number","aadhar_number","bmp_id","vender_name"],
            },
        ),
        (
            "Permissions",
            {
                "classes": ["wide"],
                "fields": ["is_active","is_email_verified","is_staff","isShopkeeper"],
            },
        )
    ]
    search_fields = ["username","first_name","last_name","email"]
    ordering = ["first_name","last_name"]
    filter_horizontal = []
    readonly_fields = ["email_token"]



@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin):
   
    list_display = ["id","username","first_name","last_name","email"]
    list_filter = ["email"]
    
    fieldsets = [
        ("User Credentials", {"fields": ["username","email", "password"]}),
        ("Personal info", {"fields": ["first_name","last_name","email_token"]}),
        ("Permissions", {"fields": ["is_active","is_staff","is_email_verified","isShopkeeper"]}),
    ]
    
    add_fieldsets = [
        (
            "User Credentials",
            {
                "classes": ["wide"],
                "fields": ["username","email", "password1", "password2"],
            },
           
            
        ),
        (
            "Personal info",
            {
                "classes": ["wide"],
                "fields": ["first_name","last_name","profile_image"],
            },
        ),
        (
            "Permissions",
            {
                "classes": ["wide"],
                "fields": ["is_active","is_email_verified","is_staff","isShopkeeper"],
            },
        )
    ]
    search_fields = ["username","first_name","last_name","email"]
    ordering = ["first_name","last_name"]
    filter_horizontal = []
    readonly_fields = ["email_token"]
