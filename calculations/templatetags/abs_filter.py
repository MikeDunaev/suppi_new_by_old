from django import template

register = template.Library()

@register.simple_tag
def abs_num(value=None):
    try:
        v = abs(int(value))
    except:
        v = 0
    return v