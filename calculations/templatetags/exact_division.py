from django import template

register = template.Library()

@register.simple_tag
def exact_divide(a ,b):
    return a // b, a % b