from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(subject,message,email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

# email_utils.py


from django.core.mail import EmailMessage

def send_email_with_attachment(subject, message, recipient_list, attachment_path):
    
    from_email=settings.EMAIL_HOST_USER
    # Read the file content in binary mode
    with open(attachment_path, 'rb') as file:
        file_content = file.read()
    
    email = EmailMessage(subject, message, from_email, recipient_list)

    email.attach(attachment_path.split('/')[-1],file_content, 'application/pdf')
   
    # Send the email
    email.send()