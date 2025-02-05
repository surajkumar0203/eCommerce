from accounts.views import register, login_page, logout_page,account_activate,shopkeeper_register,shopkeeper_login,account_user_profile
from django.urls import path

urlpatterns = [
    path('register/', register, name='register'),
    path('shopkeeper_ragister/', shopkeeper_register, name='shopkeeper_ragister'),
    path('login/', login_page, name='login_page'),
    path('shopkeeper_login/', shopkeeper_login, name='shopkeeper_login'),
    path('activate_email/<str:token_id>/', account_activate, name='account_activate'),
    path('userprofile/', account_user_profile, name='account_user_profile'),
    path('logout/', logout_page, name='logout_page'),
]