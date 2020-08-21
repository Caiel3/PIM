from django.shortcuts import render
from .models import Materiales
from django.http import HttpResponse

def index(request):
    
    return render(request,'index.html')

def subida(request):
    archivo = request.FILES["archivo"]
    tipo = request.POST["tipo"]
    ancho = request.POST["ancho"]
    largo = request.POST["largo"]
    v=Materiales.objects.filter(ean='7701520374390')
    return HttpResponse(v)
    pass