from django import template

register = template.Library()

@register.filter
def first_word(value):
   
    try:
        first= value.split(" ")[0]
        second= value.split(" ")[1]
        return "".join([first,second])
    except:
        return value


