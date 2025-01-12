from django.shortcuts import render
from products.models import Category,VendorProducts,ProductVariant
from django.db.models import Q
from orders.models import *
from accounts.models import Customer



def home(request):
    categories = Category.objects.all()
    """
    dono ka result same hoga, lekin Q objects ka use karne se code zyada readable aur maintainable hota hai.

    Use Case:
        Q objects ka use tab hota hai jab:
            Complex logic banana ho (e.g., AND aur OR ko mix karna).
            Dynamic queries likhni ho (e.g., runtime pe conditions set karni ho).
           
    """
    # products = VendorProducts.objects.filter(
    #     Q(product__parent_product__isnull=True) &
    #     Q(product__product_images__isnull=False)
    # )

    # Agar sirf AND conditions use karni hai, toh ye style zyada readable aur simple hai.
    products = VendorProducts.objects.filter(
        product__parent_product__isnull=True,
        product__product_images__isnull=False
    )
   
    context = {
        "products" : products,
    }
    return render(request, 'home/home.html',context)


def product_details(request,product_id):
    
    vendor_product=VendorProducts.objects.get(product__id=product_id)
    
    if request.GET.get('product_sku'):
        vendor_product=VendorProducts.objects.get(product__product_sku=request.GET.get('product_sku'))
      
    
    products_varients=[]
    
    if vendor_product.product.product_variants.exists():
        variant_options = vendor_product.product.product_variants.prefetch_related('variant_option')
      
        for variant_option in variant_options:
            products_varients.extend({
                'product_sku':vendor_product.product.product_sku,
                'option_name':option.option_name,
                'variant_name':option.variant_name,
            }
            for option in variant_option.variant_option.all()
            )
    
    child_vendor_product=[]
    
    if vendor_product.product.parent_product:
        child_vendor_product=[vendor_product.product]
    else: 
        child_vendor_product=vendor_product.product.variant_products.all()

    
    # child_vendor_product=sorted(child_vendor_product)
    for cvp in child_vendor_product:
        product_variant=ProductVariant.objects.filter(product=cvp).first()
       
        products_varients.extend(
        
            {
                'product_sku':cvp.product_sku,
                'option_name':option.option_name,
                'variant_name':option.variant_name,
            
            }
            for option in product_variant.variant_option.all()
        )
  

    result={}
    for variant in products_varients:
        product_sku=variant['product_sku']
        variant_string=f"{variant['variant_name']} : {variant['option_name']}"

        if product_sku in result:
            result[product_sku].append(variant_string)
        else:
            result[product_sku]=[variant_string]
# show cart_quantity (when cart_quantity==0 then Remove from Cart button will hide ) 
    cart_quantity=0
    try:
        current_customer = request.user
        my_user=Customer.objects.get(username=current_customer)

        
        cart,_=Carts.objects.get_or_create(customer=my_user)
       
        cart_item=CartItem.objects.filter(customer=cart,product=vendor_product).first()
        cart_quantity=cart_item.quantity
    except:
        pass
    
    
    context={
        "product":vendor_product,
        "product_variants_result":result,
        "cart_quantity":cart_quantity
    }
    
    return render(request, 'home/product_details.html',context)