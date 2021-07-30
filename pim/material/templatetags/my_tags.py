from django import template
from datetime import datetime

register = template.Library()

@register.filter
def modulo(num, val):
    return int(num % val)

@register.filter
def rango(num,sum):
    return str((num+sum)*100)

@register.filter
def convertir_fecha(num,fecha):
    if 'None' in str(fecha):
        return str('')
    else:
        return datetime.strftime(fecha,'%d-%m-%Y %I:%M %p')




