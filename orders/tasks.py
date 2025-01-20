from celery import shared_task
from utils.utility import generate_order_pdf,send_pdf_to_email
import time
from orders.models import Order

@shared_task
def send_Email(order_id, sender_email):
    instance=Order.objects.filter(order_id=order_id)
    # Send PDF to email
    send_pdf_to_email(sender_email,instance.first())
    
