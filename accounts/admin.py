from django.contrib import admin
from accounts.models import MyUser,Shopkeeper
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
   
    list_display = ["id","username","first_name","last_name","email","is_active","is_admin"]
    list_filter = ["email"]
    
    fieldsets = [
        ("User Credentials", {"fields": ["username","email", "password"]}),
        ("Personal info", {"fields": ["first_name","last_name","email_token"]}),
        ("Permissions", {"fields": ["is_admin","is_superuser","is_active","is_staff","is_email_verified"]}),
    ]
    
    add_fieldsets = [
        (
            "User Credentials",
            {
                "classes": ["wide"],
                "fields": ["username","email", "password"],
            },
           
            
        ),
        (
             "Personal info",
            {
                "classes": ["wide"],
                "fields": ["first_name","last_name"],
            },
        ),
        (
            "Permissions",
            {
                "classes": ["wide"],
                "fields": ["is_admin","is_superuser","is_active","is_staff"],
            },
        )
    ]
    search_fields = ["username","first_name","last_name","email"]
    ordering = ["first_name","last_name"]
    filter_horizontal = []
    readonly_fields = ["email_token"]

@admin.register(Shopkeeper)
class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ["id","gst_number","aadhar_number","profile_image","bmp_id","vender_name"]
    exclude = ["is_active","is_admin","is_staff","is_superuser","is_email_verified","email_token"]
    
    


