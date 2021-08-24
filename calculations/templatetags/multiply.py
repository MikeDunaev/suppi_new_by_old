from django import template

register = template.Library()

@register.simple_tag
def multiply_two_numbers(a, b):
    return a * b