from django.shortcuts import render,redirect
from accounts.models import MyUser as User,Customer,Shopkeeper
from products.models import *
from utils.utility import generate_code
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils.utility import is_shopkeeper


@login_required(login_url="/")
@is_shopkeeper()
def upload_product(request):
  
    if request.method=='POST':
        brand_name = request.POST.get('brand_name')
        category_name = request.POST.get('category_name')
        commission_percentage = request.POST.get('comission_percentage')
        upload_image = request.FILES.get('upload_image')
        item_name = request.POST.get('item_name')
        product_description = request.POST.get('product_description')
        parent_product = request.POST.get('parent_product')
        maximum_retail_price = request.POST.get('maximum_retail_price')
        variant_name = request.POST.get('variant_name')
        option_name = request.POST.get('option_name')
        vender_selling_price = request.POST.get('vendor_selling_price')
        dealer_price = request.POST.get('dealer_price')
        delivery_price = request.POST.get('delivery_price')
        
        # convert into decimal
        try:
            vender_selling_price=float(vender_selling_price)
            dealer_price=float(dealer_price)
            # delivery_price=float(delivery_price)
        except:
            messages.success(request,"Invalid Input")
            return redirect("/products/upload/")

        # generate Product sku and HSN CODE
        product_sku=generate_code("2DRF")
        hsn_code = generate_code()  
        
        # store in data bases
        category,_=Category.objects.get_or_create(name=category_name,comission_percentage=commission_percentage)
        brand,_=BrandName.objects.get_or_create(name=brand_name)

        if parent_product and parent_product != '--select--':  # Check if parent_product is provided
            parent_product_obj = Products.objects.get(product_sku=parent_product)  # Fetch the parent product object
        else:
            parent_product_obj = None  # Set to None if no parent product is selected
        
        product,_=Products.objects.get_or_create(
            category=category,
            brand=brand,
            item_name=item_name,
            product_description=product_description,
            product_sku=product_sku,
            hsn_code=hsn_code,
            parent_product=parent_product_obj,
            maximum_retail_price=maximum_retail_price
        )

        variant_option,_ = VariantOptions.objects.get_or_create(variant_name=variant_name, option_name=option_name)

        product_variant=ProductVariant.objects.create(product=product)
        product_variant.variant_option.set([variant_option])
        
        if upload_image:
            print(upload_image)
            # Get the file extension
            file_extension = os.path.splitext(upload_image.name)[1]
            # Create the new file name
            new_file_name = f"products/images/{product_sku}{file_extension}"
            
            # Save the uploaded image to the correct location
            file_path = default_storage.save(new_file_name, ContentFile(upload_image.read()))
            
            product_img,_=ProductImages.objects.get_or_create(product=product,image=new_file_name)
            
    
        # store vendor product
        delivery_price = float(delivery_price) if delivery_price else 0
        shopkeeper=Shopkeeper.objects.get(username=request.user)
        vender_product=VendorProducts.objects.create(
            shopkeeper=shopkeeper,
            product=product,
            vendor_selling_price=vender_selling_price,
            dealer_price=dealer_price,
            delivery_price=delivery_price
        )
        return redirect("/products/upload/")

    parent_product=Products.objects.all().distinct()

    context={
        'parent_products':parent_product
    }
    return render(request,'products/upload_products.html',context)
