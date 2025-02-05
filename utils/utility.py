from datetime import datetime
from uuid import uuid4
import pdfkit
from django.template.loader import get_template
from django.conf import settings
from utils.emails import send_email_with_attachment
from django.shortcuts import redirect


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
    

# generate code
def generate_code(value=None):
    random_value=str(uuid4()).split("-")[0]
    if value:
        return "".join([value,random_value])
    return "".join(["HSN-",random_value.upper()])

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
 
   
    send_email_with_attachment(subject, message, recipient_list, attachment_path)

    






def is_shopkeeper(required_role='shopkeeper'):
    def inner_wrapper(view_func):
        def wrapper(request,*args,**kwargs):
            if not request.user.is_authenticated:
                return redirect("/")  
            if required_role == "shopkeeper" and not request.user.isShopkeeper:
                return redirect("/")  
            if required_role == "customer" and request.user.isShopkeeper:
                return redirect("/")
            return view_func(request, *args, **kwargs)  
        return wrapper
    return inner_wrapper