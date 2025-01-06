from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email_token,email):
    send_mail(
        "Account Activation",
        f"Click here to activate your account http://127.0.0.1:8000/accounts/activate_email/{email_token}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )