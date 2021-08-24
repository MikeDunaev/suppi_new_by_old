from django import template

register = template.Library()

@register.simple_tag
def to_number(value):
    list = value.split("-")
    try:
        return int(list[1])
    except:
        return list
