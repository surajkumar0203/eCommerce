from django import template

register = template.Library()

@register.filter
def split_order(value):
    value1=str(value).split("-")[-2]
    value2=str(value).split("-")[-1]
    return "-".join(["ORD",value1,value2])

    