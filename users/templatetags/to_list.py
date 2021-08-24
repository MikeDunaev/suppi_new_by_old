from django import template

register = template.Library()

@register.simple_tag
def to_list(value):
    list_shop=[]
    for i in value:
        list_shop.append(str(i))
    return list_shop
