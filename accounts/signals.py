from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import MyUser as User,Customer,Shopkeeper
from uuid import uuid4
from utils.emails import send_account_activation_email


@receiver(post_save, sender=Shopkeeper)
@receiver(post_save, sender=Customer)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid4())
            email=instance.email
            instance.email_token=email_token
            subject="Account Activation"
            message=f"Click here to activate your account http://127.0.0.1:8000/accounts/activate_email/{email_token}",
            message=message[0]
            send_account_activation_email(subject,message,email)
    except Exception as e:
        print(e)