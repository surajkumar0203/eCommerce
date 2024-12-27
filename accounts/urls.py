from accounts.views import register, login_page, logout_page
from django.urls import path

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
]