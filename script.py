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
    
def upload_products():
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

