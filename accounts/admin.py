from django.contrib import admin
from accounts.models import MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
   
    list_display = ["id","username","first_name","last_name","email","is_active","is_admin"]
    list_filter = ["email"]
    
    fieldsets = [
        ("User Credentials", {"fields": ["username","email", "password"]}),
        ("Personal info", {"fields": ["first_name","last_name"]}),
        ("Permissions", {"fields": ["is_admin","is_superuser","is_active","is_staff"]}),
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


