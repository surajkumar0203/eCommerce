from products.models import BrandName

def brand_name(request):
    brands = BrandName.objects.all().distinct()[:5]
    return {'brands': brands}