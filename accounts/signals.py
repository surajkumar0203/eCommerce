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
            send_account_activation_email(email_token,email)
    except Exception as e:
        print(e)