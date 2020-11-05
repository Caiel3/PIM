from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    return int(num % val)

@register.filter
def rango(num,sum):
    return str((num+sum)*100)

