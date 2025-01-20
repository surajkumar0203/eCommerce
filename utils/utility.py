from datetime import datetime
from uuid import uuid4
import pdfkit
from django.template.loader import get_template
from django.conf import settings
from utils.emails import send_email_with_attachment

def generate_order_id(item_count):
    now= datetime.now()
    item_count=str(item_count).zfill(4)
    order_id = f"ORD-{now.strftime("%Y%m%d-%H%M%S")}-{item_count}"
    return order_id


# generate slug for orderItem

def generate_slug(order_id):
    order_id=str(order_id)
    order_id=order_id.split("-")
    unique=str(uuid4()).split("-")[0]
    return "".join([order_id[1],order_id[2],unique])
    

def generate_order_pdf(instance):
    templates_name = 'order/invoice'
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
   
        'no-outline': None,


    }

    path_to_wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    template = get_template(f'{templates_name}.html')
    content = template.render({'order_item':instance.get_order_data()})
    output_path = f"{settings.BASE_DIR}/public/static/pdfs/{instance.order_id}.pdf"
    
    config=pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    
    pdfkit.from_string(content,output_path,options=options,configuration=config)



# send pdf to email

def send_pdf_to_email(sender_email,instance):
    
    subject = f"Order {instance.order_id} Invoice"
    message = f"Please find the attached invoice for your order."
    recipient_list = [sender_email]  

    
    attachment_path = f"{settings.BASE_DIR}/public/static/pdfs/{instance.order_id}.pdf"  
    print(attachment_path)

    send_email_with_attachment(subject, message, recipient_list, attachment_path)

    # from_email = settings.DEFAULT_FROM_EMAIL
    # subject = f"Order {instance.order_id} Invoice"
    # message = f"Please find the attached invoice for your order."
    # attachment_path = f"{settings.BASE_DIR}/public/static/pdfs/{instance.order_id}.pdf"