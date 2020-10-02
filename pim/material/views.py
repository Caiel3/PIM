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
from reportlab.lib.units import inch 
from reportlab.platypus import Paragraph
from  reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

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
    
    file = mi_archivo.read().decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(file))
    try:
        archivo = [line for line in reader]    
    except Exception as e:
        messages.error(request,"Por favor valide bien la estructura del archivo, si el error persiste contacte con el administrador.")

       
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
    files = mi_archivo.read().decode('utf-8-sig')   
    reader = csv.DictReader(io.StringIO(files),fieldnames=None,delimiter=';')
    archivo = [line for line in reader]     
    try:          
         #insertamos temporamente datos en una tabla para despues traerlos ordenados de una manera mas cesilla
        carga_temp=[line for line in archivo]    
        Catalogo_temp.objects.all().delete()          
        for dato in carga_temp:        
            Catalogo_temp.objects.create(material=dato['Material'],unidad_empaque=dato['Unidad de empaque'],coleccion=dato['Colección'],precio=dato['Precio'],moneda='',pais=dato['Pais'])

        
        header_consulta_material=[]
        for valor in archivo:
            header_consulta_material.append(valor['Material'])
            pass               
       
        """ 26 px de diferencia en la tercera marca """
        datosGEF=consulta_marca_catalogo('GEF')
        datosBF=consulta_marca_catalogo('BABY FRESH')
        datosPB=consulta_marca_catalogo('PUNTO BLANCO')
        can_marca=np.asarray(consultasql(" SELECT COUNT(MARCA) AS CANTIDAD,MARCA FROM RAM.CATALOGO GROUP BY MARCA order by MARCA"))
        con=0
        bfh=0# hojas Baby fresh
        pbh=0#hojas Punto blanco
        gefh=0#hojas gef
        cantidad_marcas=consultasql("SELECT COUNT(*) FROM ( SELECT COUNT(MARCA) AS CANTIDAD,MARCA FROM RAM.CATALOGO GROUP BY MARCA order by MARCA) CAM")
        can=[li for li in cantidad_marcas]
        
        for marca in can_marca:             
            if marca[1]=='BABY FRESH':
                bfh=(converts_helper.numero_paginas_marca(int(marca[0])))                
                pass
            elif marca[1]=='PUNTO BLANCO':
                pbh=(converts_helper.numero_paginas_marca(int(marca[0])))                
            else:                
                gefh=(converts_helper.numero_paginas_marca(int(marca[0])))            
                if can[0][0]==3:
                    gefh=gefh-26
                
                pass                  
                
        return render(request,'catalogo.html',{'datosGEF' : datosGEF,'datosPB' : datosPB,'datosBF' : datosBF,'Cgef':'height:{}px;'.format(gefh),'CPb':'height:{}px;'.format(pbh),'Cbf':'height:{}px;'.format(bfh),'moneda':dato['Moneda']})
    except Exception as e:        
        if type(e) is KeyError:
            messages.error(request,'Recuerde que debe de conservar la estructura del archivo plano y este debe de estar separado por ;, error cerca a {}.'.format(e))   
        elif "PRIMARY" in str(e):
            messages.error(request,'Hay un material duplicado, recuerde que deben ser unicos')
        else:
            messages.error(request,'Ocurrio un error inesperado, por favor contacte con Helpy y proporcione este error; {}'.format(e))         
            
        return render(request,'index.html')  
   
def handler404_page(request):
    return render(request, '404.html', status=404)
    
def consulta_marca_catalogo(marca):    
    consulta=("SELECT * FROM CATALOGO WHERE MARCA='{}'ORDER BY MARCA,cast(PAIS as unsigned)").format(marca)
    datos=consultasql(consulta)
    consulta_temp=[]
    for dato in np.asarray(datos):
        if MysqlColores.objects.filter(material=dato[0]).values('icono_color'):
            dato[6]=[a for a in MysqlColores.objects.filter(material=dato[0]).values('icono_color')]
            consulta_temp.append(dato)        
    datos=consulta_temp
    datos=cloud.convertir_matriz(datos,['','','','','','','','','','IMAGEN_GRANDE'],248,326,'aatdtkgdoo')
    return datos



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

def reportenuevo(request):
    
    footers=["https://www.puntoblanco.com.co/wcsstore/DefaultStorefrontAssetStore8/images/PBC/HOMEPAGE/2016/06_JUNIO/SEMANA_24/logo_PBC.jpg"
            ,"https://www.gef.com.co/wcsstore/CrystalCo/images/GEF/CABECERA/logo_gef.png"
            ,"https://tienda.babyfresh.com.co/wcsstore/DefaultStorefrontAssetStore8/images/BBF/LOGO/Logo-BF-tienda-virtuales-FEP-8.png"    ]
    doc = canvas.Canvas("Hola Mundo.pdf")
    doc.setPageSize((1190,1690))   
    encabezado(doc,footers[0])
    print(A4)
    
    """     p = ParagraphStyle('test')
    p.textColor = 'black'
    
    p.borderWidth = 0.1
    p.alignment = TA_CENTER
    p.fontSize = 14
    p2 = ParagraphStyle('test')
    p2.textColor = 'black'
    p2.borderColor = 'black'
    p2.borderWidth = 0.1
    p2.alignment = TA_CENTER
    p2.fontSize = 18


    doc.drawImage("https://aatdtkgdoo.cloudimg.io/v7/http://tienda.babyfresh.com.co/wcsstore/CrystalCo_CAT_AS//BBF/ES-CO/Imagenes/Unisex/Accesorios/Osito/566x715/Osito-Peluche-8217-Frente-Baby-Fresh.jpg?sharp=1&width=248&height=326",20,1299)

    #Nombre
    nom = Paragraph("Peluche Osito Habano Peluche Osito Habano", p)
    nom.wrapOn(doc,248,0)
    nom.drawOn(doc,20,1300)1300
    doc.line(20,1296,248,1296)-4
    #Categoria
    cat = Paragraph("Categoria: {}".format('None'), p)
    cat.wrapOn(doc,248,0)
    cat.drawOn(doc,20,1280)-20
    doc.line(20,1276,248,1276)-24
    #Material
    mat = Paragraph("Material: {}".format('602537'), p)
    mat.wrapOn(doc,248,0)
    mat.drawOn(doc,20,1263)-37
    doc.line(20,1259,248,1259)-41
    #Composición
    mat = Paragraph("composicion: {}".format('100% POLIESTER'), p)
    mat.wrapOn(doc,248,0)
    mat.drawOn(doc,20,1218)-82
    doc.line(20,1215,248,1215)-85
    #Unidad de empaque
    un = Paragraph("Unidad de empaque: {}".format('1'), p)
    un.wrapOn(doc,248,0)
    un.drawOn(doc,20,1201)-99
    doc.line(20,1197,248,1197)-103
    #Color
    col = Paragraph("Colores: {}".format(''), p)
    col.wrapOn(doc,248,0)
    col.drawOn(doc,20,1169)-131
    doc.line(20,1625,248,1665)-135
    #Tallas
    talla = Paragraph("Tallas: {}".format('UNICA'), p)
    talla.wrapOn(doc,248,0)
    talla.drawOn(doc,20,1138)-162
    doc.line(20,1135,248,1135)-165
    #Precio
    pre = Paragraph("Precio: {}".format('$ 82.992'), p2)
    pre.wrapOn(doc,248,0)
    pre.drawOn(doc,20,1120)-180
    """
    item(20,248,0,1300,doc)
    """ item(300,248,0,1300,doc)
    item(20,248,0,400,doc)
    item(300,248,0,400,doc) """
#Guardamos el documento
    doc.save()


def encabezado(doc,marca):
    doc.drawImage(marca,1,1630,240,60)
    doc.line(2,1628,1188,1628)


def item(x,y,ix,iy,doc):
    doc.drawImage("https://aatdtkgdoo.cloudimg.io/v7/http://tienda.babyfresh.com.co/wcsstore/CrystalCo_CAT_AS//BBF/ES-CO/Imagenes/Unisex/Accesorios/Osito/566x715/Osito-Peluche-8217-Frente-Baby-Fresh.jpg?sharp=1&width=248&height=326",x,iy-1)
    
    p = ParagraphStyle('test')
    p.textColor = 'black'
    
    p.borderWidth = 0.1
    p.alignment = TA_CENTER
    p.borderColor = 'black'
    p.fontSize = 14
    p2 = ParagraphStyle('test')
    p2.textColor = 'black'
    p2.borderColor = 'black'
    p2.borderWidth = 0.1
    p2.alignment = TA_CENTER
    p2.fontSize = 18


    doc.drawImage("https://aatdtkgdoo.cloudimg.io/v7/http://tienda.babyfresh.com.co/wcsstore/CrystalCo_CAT_AS//BBF/ES-CO/Imagenes/Unisex/Accesorios/Osito/566x715/Osito-Peluche-8217-Frente-Baby-Fresh.jpg?sharp=1&width=248&height=326",20,1299)

    #Nombre
    nom = Paragraph("Peluche Osito Habano Peluche Osito Habano", p)
    nom.wrapOn(doc,y,0)
    nom.drawOn(doc,x,iy)
    doc.line(x,iy-4,y,iy-4)
    #Categoria
    cat = Paragraph("Categoria: {}".format('None'), p)
    cat.wrapOn(doc,y,0)
    cat.drawOn(doc,x,iy-20)
    doc.line(x,iy-24,y,iy-24)
    #Material
    mat = Paragraph("Material: {}".format('602537'), p)
    mat.wrapOn(doc,y,0)
    mat.drawOn(doc,x,iy-37)
    doc.line(x,iy-41,y,iy-41)
    #Composición
    mat = Paragraph("Composicion: {}".format('100% POLIESTER'), p)
    mat.wrapOn(doc,y,0)
    mat.drawOn(doc,x,iy-82)
    doc.line(x,iy-85,y,iy-85)
    #Unidad de empaque
    un = Paragraph("Unidad de empaque: {}".format('1'), p)
    un.wrapOn(doc,y,0)
    un.drawOn(doc,x,iy-99)
    doc.line(x,iy-103,y,iy-103)
    #Color
    col = Paragraph("Colores: {}".format(''), p)
    col.wrapOn(doc,y,0)
    col.drawOn(doc,x,iy-131)
    doc.line(x,iy-135,y,iy-135)
    #Tallas
    talla = Paragraph("Tallas: {}".format('UNICA'), p)
    talla.wrapOn(doc,y,0)
    talla.drawOn(doc,x,iy-162)
    doc.line(x,iy-165,y,iy-165)
    #Precio
    pre = Paragraph("Precio: {}".format('$ 82.992'), p2)
    pre.wrapOn(doc,y,0)
    pre.drawOn(doc,x,iy-180)