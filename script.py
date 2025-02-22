from products.models import *
"""
This script imports necessary modules and models for the E-commerce project.
Modules imported:
- products.models: Imports all models from the products app.
- pandas as pd: Imports the pandas library for data manipulation and analysis.
- django.db.transaction: Imports the transaction module from Django's database package for handling database transactions.
"""
import pandas as pd
from django.db import transaction
import random

"""
    Import pillow library for image processing/uploading
"""
from PIL import Image

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import os


VOLUME_CHOICES = ["500ml", "1L", "2L", "250ml", "100ml"]

COLOR_CHOICES = ["Red", "Blue", "Green", "Yellow"]

WEIGHT_CHOICES = ["500g", "1kg", "2kg"]

def generate_random_options(variant_name):
    """
        This function generates random variant options for the products.
        It returns a list of dictionaries containing variant names and option names.
    """
    if variant_name == "Volume":
        return random.choice(VOLUME_CHOICES)
    elif variant_name == "Display weight":
        return random.choice(WEIGHT_CHOICES)
    elif variant_name == "Colour":
        return random.choice(COLOR_CHOICES)
    else:
        return f"{variant_name}-{random.randint(1, 100)}"
    
def upload_products():   #1
    """
        This function uploads products to the database.
        It reads a CSV file containing product details and uploads the products to the database.
    """
        
    df = pd.read_excel("products.xlsx")
    try:
        
        for index, row in df.iterrows():
            with transaction.atomic():
                category,_=Category.objects.get_or_create(name=row["Material category"])
                
                subcategory,_=SubCategory.objects.get_or_create(name=row["Sub category level 1"], category=category)
                brand,_=BrandName.objects.get_or_create(name=row["Brand name"])
                
                if row["Variation type"] in ["Parent only","Parent with variant/s"]:
                    product,_=Products.objects.get_or_create(
                        category=category,
                        sub_category=subcategory,
                        brand=brand,
                        item_name=row["Item name title"],
                        product_description=row["Product description"],
                        product_sku=row["Product SKU"],
                        hsn_code=row["HSN code"],
                        maximum_retail_price=random.randint(5000, 260000)
                    )
                    
                    if row["Variation type"]=="Parent with variant/s":
                        variant_options = row["Variation_theme"].split("+")
                        for variant_option in variant_options:
                            option_name = generate_random_options(variant_option)
                            variant_option,_ = VariantOptions.objects.get_or_create(variant_name=variant_option, option_name=option_name)
                
                if row["Variation type"] == "Variant":
                    
                    product=Products.objects.get(product_sku=row["Parent SKU"])
                    Voptions =[]
                    variant_options = row["Variation_theme"].split("+")
                    for variant_option in variant_options:
                        option_name = generate_random_options(variant_option)
                        Variant_Option,_ = VariantOptions.objects.get_or_create(variant_name=variant_option, option_name=option_name)
                        Voptions.append(Variant_Option)
                    
                        varient_products=Products.objects.create(
                            category=category,
                            sub_category=subcategory,
                            brand=brand,
                            item_name=row["Item name title"],
                            product_description=row["Product description"],
                            product_sku=row["Product SKU"],
                            hsn_code=row["HSN code"],
                            parent_product=product,
                            maximum_retail_price=random.randint(5000, 260000)
                        )
                        product_variant=ProductVariant.objects.create(product=varient_products)
                        product_variant.variant_option.add(*Voptions)
            
    except Exception as e: 
        print(e)

# create vendor products
def vendor_products():  #3
    shopkeeper = Shopkeeper.objects.first()
    products=Products.objects.all()
    for product in products:
        VendorProducts.objects.get_or_create(
            shopkeeper=shopkeeper,
            product=product,
            vendor_selling_price=random.randint(5000, 10000),
            dealer_price=random.randint(3000, 5000)
        )


# upload image into products models

def list_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append({
                "path": os.path.join(root, file),
                "name": file
            })

    return all_files

def getProductFromImage(image_name):
    try:
        product_sku = image_name.split(".")[0]
        product = Products.objects.get(product_sku=product_sku)
        return True, product,image_name
    except Exception as e:
        pass
    return False, image_name.split(".")[0], "image_name"


# to check file is image or not
def isImage(file):
    try:
        with Image.open(file) as img:
            img.verify()
            return True
    except Exception as e:
        return False


def upload_images(path):
    file_list=list_files(path)
    for file in file_list:
        if isImage(file["path"]):
            try:
                product_image=getProductFromImage(file["name"])
                
                if product_image[0]:
                    product_obj = product_image[1]
                    
                    with open(file["path"], "rb") as f:
                        # image = File(f)
                        image = SimpleUploadedFile(file["name"], f.read())
                        
                        # print("image -> ",image)
                        # print("file -> ",f)
                    
                        ff=ProductImages.objects.create(product=product_obj, image=image)
                        print(ff)
            except Exception as e:
                pass
# upload_images("./images")  #2

# import razorpay

# client = razorpay.Client(auth=(config('RazorPay_YOUR_API_KEY'), "y95DZU1zBhOb8ciPOY8grTE7"))

# from decouple import config

# o=client.order.create({
#   "amount": 50000,
#   "currency": "INR",
#   "receipt": "receipt#1",
#   "partial_payment":False,
#   "notes": {
    
#   }
# })

# print(o)


from orders.models import Order
import pdfkit
from django.template.loader import get_template
from django.conf import settings
def generate_order_pdf(instance):
    # print(order_data)
    templates_name = 'order/invoice'

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.7in',
        'margin-bottom': '0.7in',
        'margin-left': '0.7in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
   
        'no-outline': None,

    }

    path_to_wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    template = get_template(f'{templates_name}.html')

    # print(template)

    content = template.render({"order_item":instance.get_order_data()})
    # print(content)
  
    output_path = f"{settings.BASE_DIR}/public/static/pdfs/{instance.order_orderItem.all().first().slug}.pdf"
    # print(output_path)
    config=pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    # print(config)
    try:
        pdfkit.from_string(content,output_path,options=options,configuration=config)
    except Exception as e:
        print(f"PDF generation failed: {e}")

# order=Order.objects.first()
# print(order.get_order_data())
# print(order.order_orderItem.all().first().product.delivery_price)
# print(order.order_orderItem.slug)
# generate_order_pdf(order)