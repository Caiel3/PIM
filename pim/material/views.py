from django.shortcuts import render,redirect
from .models import Materiales,Descarga,Catalogo_temp,MysqlColores
from django.http import HttpResponse,HttpResponseNotFound
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
from django.views.defaults import page_not_found
from django.template.defaultfilters import linebreaksbr, urlize

converts_helper=Converts()
cloud=CloudImage()

class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class=MaterialSerializar
    queryset = Materiales.objects.raw('select * from material_materiales limit 10')




def index(request):  
    Catalogo_temp.objects.all().delete()   
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
        return render(request,'index.html',{'ancho':ancho,'largo':largo,'tipo':tipo,'consulta':parametros})          
    #Relizamos la consulta nativa en la base de datos      
    string_campos=converts_helper.convert_array_string(parametros,tipo) #no spermite traer un string de campos a partir de un arreglo
    if string_campos=='':
        string_campos='material'
        pass
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
    
    informacion=cloud.convertir_matriz(matconsulta,parametros,ancho,largo,'aatdtkgdoo')      
    return render(request,'visualizacion.html',{"headers":parametros,"lista":informacion,"descarga":consulta_descarga})    
    pass

def Catalogoh(request):
    mi_archivo=request.FILES["archivo"]     
    files = mi_archivo.read().decode('latin1')
    reader = csv.DictReader(io.StringIO(files),fieldnames=None,delimiter=';')
    archivo = [line for line in reader]  

    try:          
         #insertamos temporamente datos en una tabla para despues traerlos ordenados de una manera mas cesilla
        carga_temp=[line for line in archivo]    
        Catalogo_temp.objects.all().delete()          
        for dato in carga_temp:        
            Catalogo_temp.objects.create(material=dato['Material'],unidad_empaque=dato['Unidad de empaque'],coleccion=dato['Colección'],precio=dato['Precio'],moneda=dato['Moneda'],pais=dato['Pais'])

        
        header_consulta_material=[]
        for valor in archivo:
            header_consulta_material.append(valor['Material'])
            pass               

        consulta=('SELECT * FROM CATALOGO ORDER BY MARCA DESC, COLECCION DESC, DEPARTAMENTO DESC, TIPO_PRENDA DESC,DESCRIPCION_MATERIAL ASC ')        
        datos=consultasql(consulta)
        consulta_temp=[]
        for dato in np.asarray(datos):
            dato[6]=[a for a in MysqlColores.objects.filter(material=dato[0]).values('icono_color')]
            consulta_temp.append(dato)
        datos=consulta_temp
   
        can_marca=np.asarray(consultasql('SELECT COUNT(MARCA) AS CANTIDAD,MARCA FROM RAM.CATALOGO GROUP BY MARCA'))
        con=0
        bfh=0# hojas Baby fresh
        pbh=0#hojas Punto blanco
        gefh=0#hojas gef
        for marca in can_marca:
            if marca[1]=='BABY FRESH':
                bfh=(converts_helper.numero_paginas_marca(int(marca[0]))*1500)
                pass
            elif marca[1]=='PUNTO BLANCO':
                pbh=(converts_helper.numero_paginas_marca(int(marca[0]))*1500)
                pass
            else:
                gefh=(converts_helper.numero_paginas_marca(int(marca[0]))*1500)      
                pass        
        datos=cloud.convertir_matriz(datos,['','','','','','','','','','IMAGEN_GRANDE'],280,358,'aatdtkgdoo')      
        return render(request,'catalogo.html',{'datos' : datos,'Cgef':'height:{}px;'.format(gefh),'CPb':'height:{}px;'.format(pbh),'Cbf':'height:{}px;'.format(bfh)})
    except Exception as e:        
        
        if type(e) is KeyError:
            messages.error(request,'Recuerde que debe de conservar la estructura del archivo plano y este debe de estar separado por ;, error cerca a {}.'.format(e))   
        else :
            messages.error(request,'Ocurrio un error inesperado, por favor contacte con Helpy y proporcione este error; {}'.format(e))         
            
        return render(request,'index.html')  
   
def handler404_page(request):
    return render(request, '404.html', status=404)
    


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

