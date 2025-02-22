from django import template

register = template.Library()

@register.filter
def aadhar_hide(value):
    temp=value.split("-")[-1]
    return f"XXXX-XXXX-{temp}"
    