from django.shortcuts import render,redirect
from .models import Materiales,Descarga,Catalogo_temp
from django.http import HttpResponse
import numpy as np
import os
from .helpers.CloudImage import CloudImage
from .helpers.converts import Converts
from .helpers.descarga_imagenes import Descarga_imagenes
from django.db import connection
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,mm
import csv
import io
from django.contrib import messages
from rest_framework import viewsets
from .serializar import MaterialSerializar
import numpy as np



converts_helper=Converts()


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class=MaterialSerializar
    queryset = Materiales.objects.raw('select * from material_materiales limit 10')




def index(request):    
    return render(request,'index.html')

def subida(request):
    consulta=[
        'MATERIAL',
        'DESCRIPCION_MATERIAL',
        'DESCRIPCION_MATERIAL_ENRIQUECIDO',
        'DESCRIPCION_LARGA',
        'EAN',
        'DESCRIPCION_TALLA',
        'DESCRIPCION_COLOR',
        'IMAGEN_GRANDE',
        'TIPO_PRENDA',
        'SUBGRUPO',
        'GENERO',
        'DEPARTAMENTO',
        'CARACTERISTICA',
        'TAGS',
        'GRUPO_DESTINO'
        ]
    parametros=[]
    #Capturamos la informacion del formulario    
    archivo = request.FILES["archivo"]     
    tipo = request.POST["tipo"]
    ancho = request.POST["ancho"]
    largo = request.POST["largo"]   
    for item in consulta:
        if item.upper() in request.POST :
            aux=request.POST[item]
            parametros.append(aux)                            
        pass             
    mi_archivo=request.FILES["archivo"] 
    file = mi_archivo.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file))
    archivo = [line for line in reader]   
    vali=validacion(archivo,tipo)
    if vali:
        messages.error(request,vali)
        print(parametros)
        return render(request,'index.html',{'ancho':ancho,'largo':largo,'tipo':tipo,'consulta':parametros})          
    #Relizamos la consulta nativa en la base de datos      
    string_campos=converts_helper.convert_array_string(parametros,tipo) #no spermite traer un string de campos a partir de un arreglo
    string_filtro=converts_helper.convert_array_string(archivo,tipo,False)
    vector_consulta_descarga=Converts.convert_dic_array(archivo,tipo)    
    #controlo por donde hace la consulta si por ean o material   
    if tipo =="MATERIAL":        
        consulta='select distinct {} from material_materiales where material in ({});'.format(string_campos,string_filtro)       
        consulta_descarga=Materiales.objects.values('ean','imagen_grande').filter(material__in=vector_consulta_descarga)        
                   
    else:
        consulta='select distinct {} from material_materiales where ean in ({});'.format(string_campos,string_filtro)       
        consulta_descarga=Materiales.objects.values('ean','imagen_grande').filter(ean__in=vector_consulta_descarga)       
    #Guardarmos lo que se va a descargar en la base de datos por si se descarga
   
    Descarga.objects.all().delete()
    for valor in consulta_descarga:
        Descarga.objects.create(ean=valor['ean'],imagen_grande="https://{}.cloudimg.io/v7/{}?sharp=1&width={}&height={}".format('aatdtkgdoo',valor['imagen_grande'],ancho,largo))        
    matconsulta=consultasql(consulta)    
    #converitmos todo haciendo uso de cloud img  
    cloud=CloudImage()
    informacion=cloud.convertir_matriz(matconsulta,parametros,ancho,largo,'aatdtkgdoo')      
    return render(request,'visualizacion.html',{"headers":parametros,"lista":informacion,"descarga":consulta_descarga})    
    pass

def Catalogoh(request):
    mi_archivo=request.FILES["archivo"]     
    files = mi_archivo.read().decode('latin1')
    reader = csv.DictReader(io.StringIO(files),fieldnames=None,delimiter=';')
    archivo = [line for line in reader]  

    #insetamos temporamente datos en una tabla para despues traerlos ordenados de una manera mas cesilla
    carga_temp=[line for line in archivo]    
    Catalogo_temp.objects.all().delete()  
    for dato in carga_temp:        
        Catalogo_temp.objects.create(material=dato['Material'],unidad_empaque=dato['Unidad de empaque'],coleccion=dato['Colección'],precio=dato['Precio'],moneda=dato['Moneda'],pais=dato['Pais'])


    header_consulta_material=[]
    for valor in archivo:
        header_consulta_material.append(valor['Material'])
        pass
  
    consulta=('SELECT * FROM CATALOGO ORDER BY MARCA DESC, COLECCION DESC, DEPARTAMENTO DESC, TIPO_PRENDA DESC,DESCRIPCION_MATERIAL ASC')
    datos=consultasql(consulta)   
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=catalogo.pdf'
    archivo=['100243','1003','100304','100308','100309','100326','100344','10036','100361','100378','100396']  
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    y = 740
    registroxhoja= 0
    c.setLineWidth(.3)
    c.setFont('Helvetica-Bold',11)
    for val in datos:
        if registroxhoja == 4:
            registroxhoja = 0
            y = 740
            c.showPage()
        
        c.drawImage(val[9], 35, y-130, 140, 160)
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Categoria:')
        c.setFont('Helvetica',11)
        c.drawString(245,y,val[11])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Colección:')
        c.setFont('Helvetica',11)
        c.drawString(245,y,val[5])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Material:')
        c.setFont('Helvetica',11)
        c.drawString(230,y,val[0])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Composición:')
        c.setFont('Helvetica',11)
        c.drawString(265,y,val[5])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Unidad de empaque:')
        c.setFont('Helvetica',11)
        c.drawString(300,y,val[1])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Color:')
        c.setFont('Helvetica',11)
        c.drawString(220,y,val[6])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Tallas:')
        c.setFont('Helvetica',11)
        c.drawString(220,y,val[7])
        y = y - 40
        c.line(35,y,560,y)
        y = y - 40
        registroxhoja = registroxhoja+1

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    


def consultasql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        mat=cursor.fetchall()
    pass
    return mat

def descarga(request):
    
    descarga=Descarga_imagenes()
    descarga.descargar(Descarga.objects.values('ean','imagen_grande').all())
    return render(request,'index.html')
    

def validacion(lista,tipo):        
    if lista:
        if len(lista[0].keys())>1:
            return('Recuerde que solo puede ingresar una lista de eans o materiales, la que tiene actualmente tiene mas de 1 columna')
        else:
            keys=[]
            for li in lista[0]:
                keys.append(li)
                pass 
            con=Converts()
            llave=con.convert_array_string(keys,"")                   
            if(tipo not in  llave.upper()):
                return('Usted seleciono un header {} y ingreso un archivo con header {}, por favor valide.').format(tipo,llave)
            else:
                return (False)
    else:
        return('El documento esta vacio por favor valide')
    pass

