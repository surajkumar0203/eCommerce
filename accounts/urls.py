from accounts.views import register, login_page, logout_page,account_activate
from django.urls import path

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_page, name='login_page'),
    path('activate_email/<str:token_id>/', account_activate, name='account_activate'),
    path('logout/', logout_page, name='logout_page'),
]