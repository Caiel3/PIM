import pdb
from django.shortcuts import render,redirect
from .models import Materiales,Descarga,Catalogo_temp,MysqlColores,Marca,Genero,Grupo_Destino,Tipo_Prenda
from django.http import HttpResponse,HttpResponseNotFound
from .helpers.CloudImage import CloudImage
from .helpers.converts import Converts
from .helpers.descarga_imagenes import Descarga_imagenes
from .helpers.limpiar import Limpiar
from .helpers.TxtControlador import Txt
from .helpers.csv_pim import csv_pim
from django.db import connection
from django.http import HttpResponse,FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,mm
from django.contrib import messages
from rest_framework import viewsets
from django.views.defaults import page_not_found
from django.template.defaultfilters import linebreaksbr, urlize
from django.conf import settings
from reportlab.lib.units import inch 
from reportlab.platypus import Paragraph
from  reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from .helpers.claves import Claves
import numpy as np
import os
import csv
import io
from .serializar import MaterialSerializar
import numpy as np
from datetime import datetime
import uuid
import asyncio
import threading
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from math import  ceil

converts_helper=Converts()
cloud=CloudImage()

class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class=MaterialSerializar
    queryset = Materiales.objects.raw('select * from material_materiales limit 10')

def index(request):  
    Catalogo_temp.objects.all().delete()
    Limpiar.limpiar_media_imagenes()
    marcas=Marca.objects.all()        
    genero=Genero.objects.all()
    grupo_Destino=Grupo_Destino.objects.all()
    tipo_Prenda=Tipo_Prenda.objects.all()

   
    return render(
        request,
        'index.html',
            {'marcas':marcas,                      
            "generos":genero,
            "grupo_destinos":grupo_Destino,
            "tipo_prendas":tipo_Prenda})

def subida(request):
    try:        
        inicio= datetime.now()  
        marcas=Marca.objects.all()        
        genero=Genero.objects.all()
        grupo_Destino=Grupo_Destino.objects.all()
        tipo_Prenda=Tipo_Prenda.objects.all()
        Txt('prueba','INICIO', datetime.now(),datetime.now())
        inicio= datetime.now()   
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
            'MARCA',
            'DEPARTAMENTO',
            'CARACTERISTICA',
            'TAGS',
            'GRUPO_DESTINO',
            'TIPO_MATERIAL',
            'COMPOSICION_ES',
            'ORIGEN',
            'URL_IMAGEN'
            ]
 
        parametros=[]       

        #Capturamos la informacion del formulario          
        tipo = request.POST["tipo"]
        ancho = request.POST["ancho"]
        largo = request.POST["largo"] 
        ean_consulta = request.POST["Ean_Consul"]  
        for item in consulta:
            if item.upper() in request.POST :
                aux=request.POST[item]
                parametros.append(aux)                            
            pass
            
        if len(request.FILES)!=0 and tipo =='':
            messages.error(request,'Por favor seleccione el medio de consulta.')
            return render(
                request,
                'index.html',
                {'ancho':ancho,
                'largo':largo,
                'tipo':tipo,
                'consulta':parametros,
                'mostrar':'no',
                'marcas':marcas,                      
                "generos":genero,
                "grupo_destinos":grupo_Destino,
                "tipo_prendas":tipo_Prenda
               })
        
        if len(request.FILES)!=0 or tipo !='':
                if request.POST['Ean_Consul']!= '':
                    messages.error(request,'Por favor verifique como desea hacer la consulta si por ean o por archivo.')
                    return render(
                            request,
                            'index.html',
                            {'ancho':ancho,
                            'largo':largo,
                            'tipo':tipo,
                            'consulta':parametros,
                            'mostrar':'no',
                            'marcas':marcas,                      
                            "generos":genero,
                            "grupo_destinos":grupo_Destino,
                            "tipo_prendas":tipo_Prenda
                            })

        
        if len(request.FILES)==0:
            count=0
            if (request.POST['DWMarca']!=''):
                count=count+1
            if (request.POST['DWGenero']!=''):
                count=count+1
            if (request.POST['DWGrupo_destino']!=''):
                count=count+1
            if (request.POST['DWTipo_prenda']!=''):
                count=count+1
            if(request.POST['Ean_Consul']!=''):
                count=count+1
            
            if request.POST['DWMarca']!= '' or request.POST['DWGenero']!='' or request.POST['DWGrupo_destino']!='' or request.POST['DWTipo_prenda']!='' :
                if request.POST['Ean_Consul']!= '':
                    messages.error(request,'Por favor verifique como desea hacer la consulta si por ean o selección.')
                    return render(
                        request,
                        'index.html',
                        {'ancho':ancho,
                        'largo':largo,
                        'tipo':tipo,
                        'consulta':parametros,
                        'mostrar':'no',
                        'marcas':marcas,                      
                        "generos":genero,
                        "grupo_destinos":grupo_Destino,
                        "tipo_prendas":tipo_Prenda
                        })


            if count==0:            
                messages.error(request,'Por favor seleccione un medio de consulta, sea subir el archivo, ingresar los eans  o seleccionar en las listas deplegables.')
                return render(
                    request,
                    'index.html',
                    {'ancho':ancho,
                    'largo':largo,
                    'tipo':tipo,
                    'consulta':parametros,
                    'mostrar':'no',
                    'marcas':marcas,                      
                    "generos":genero,
                    "grupo_destinos":grupo_Destino,
                    "tipo_prendas":tipo_Prenda})

           
      
      
        string_campos=converts_helper.convert_array_string(parametros,tipo,",") #nos permite traer un string de campos a partir de un arreglo
        if string_campos=='':
            string_campos='ean,imagen_grande'
            parametros=['EAN','IMAGEN_GRANDE']   
            pass
        else:
            parametros=['EAN','IMAGEN_GRANDE']+parametros 
            string_campos='ean,imagen_grande,'+string_campos
        Txt('prueba','Valida informacion e inicializa campos.', inicio,datetime.now())    
        inicio= datetime.now() 
        if len(request.FILES)!=0 and request.POST["Ean_Consul"]== '' :   # si carga un archivo entra aqui         
            mi_archivo=request.FILES["archivo"]            
            try:
                file = mi_archivo.read().decode('utf-8-sig')
                reader = csv.DictReader(io.StringIO(file))    
                archivo = [line for line in reader]    
            except Exception as e:
                messages.error(request,"Por favor valide bien la estructura del archivo, si el error persiste contacte con el administrador. y disponga este error:{}".format(e))
                return render(
                request,
                'index.html',
                {'ancho':ancho,
                'largo':largo,
                'tipo':tipo,
                'consulta':parametros,
                'mostrar':'no',
                'marcas':marcas,                      
                "generos":genero,
                "grupo_destinos":grupo_Destino,
                "tipo_prendas":tipo_Prenda})
            Txt('prueba','Se lee el archivo de consulta', inicio,datetime.now())
            inicio= datetime.now()  
            
            vali=Validacion(archivo,tipo)
            if vali:
                messages.error(request,vali)       
                return render(
                request,
                'index.html',
                {'ancho':ancho,
                'largo':largo,
                'tipo':tipo,
                'consulta':parametros,
                'mostrar':'no',
                'marcas':marcas,                      
                "generos":genero,
                "grupo_destinos":grupo_Destino,
                "tipo_prendas":tipo_Prenda
               })   
            Txt('prueba','Valida la estructura del archivo', inicio,datetime.now())
            inicio= datetime.now()        
            #Relizamos la consulta nativa en la base de datos      
           
            string_filtro=converts_helper.convert_array_string(archivo,tipo,',',False)
          
            Txt('prueba','Prepara los campos por el que se hace la consulta', inicio,datetime.now())
            inicio= datetime.now() 
            Txt('prueba','Valida las estruturas de consulta y lee el archivo que se carga.', inicio,datetime.now())    
            inicio= datetime.now()    
            #controlo por donde hace la consulta si por ean o material   
            if tipo =="MATERIAL":
                if Consulta_Where_Cantidad(request.POST['DWMarca'],request.POST['DWGenero'],request.POST['DWGrupo_destino'],request.POST['DWTipo_prenda'])!=0:
                    consulta='select distinct {} from material_materiales where material in ({}) and {};'.format(string_campos,string_filtro,Consulta_Where(request.POST['DWMarca'],request.POST['DWGenero'],request.POST['DWGrupo_destino'],request.POST['DWTipo_prenda']))        
                else:
                    consulta='select distinct {} from material_materiales where material in ({});'.format(string_campos,string_filtro) 
                                    
            else:
                if Consulta_Where_Cantidad(request.POST['DWMarca'],request.POST['DWGenero'],request.POST['DWGrupo_destino'],request.POST['DWTipo_prenda'])!=0:
                    consulta='select distinct {} from material_materiales where ean in ({}) and {}; '.format(string_campos,string_filtro,Consulta_Where(request.POST['DWMarca'],request.POST['DWGenero'],request.POST['DWGrupo_destino'],request.POST['DWTipo_prenda']))                     
                else:
                    consulta='select distinct {} from material_materiales where ean in ({});'.format(string_campos,string_filtro,) 

            matconsulta=consultasql(consulta)  
        elif request.POST['Ean_Consul']!= "":
            array_filt=converts_helper.convert_string_array(ean_consulta)
            string_filtro_ean=converts_helper.convert_array_str(array_filt,',',False)
            consulta='select distinct {} from material_materiales where ean in ({});'.format(string_campos,string_filtro_ean) 
            matconsulta=consultasql(consulta)
            # import pdb; pdb.set_trace()

        else:
            consulta='select distinct {} from material_materiales where {};'.format(string_campos,Consulta_Where(request.POST['DWMarca'],request.POST['DWGenero'],request.POST['DWGrupo_destino'],request.POST['DWTipo_prenda']))
            matconsulta=consultasql(consulta)    


 

                
        Txt('prueba','Realiza la consulta en la base de datos', inicio,datetime.now())
        inicio= datetime.now()        
            
        #converitmos todo haciendo uso de cloud img  
        
        informacion=cloud.convertir_matriz(
            matconsulta,
            1,
            ancho,
            largo,
            Claves.get_secret('CLOUDIMG_TOKEN'))      
        hash_archivo = str(uuid.uuid1())
        Txt('prueba','Resizen cloud img', inicio,datetime.now())
        inicio= datetime.now()         
        rango=list(range(0,ceil(len(informacion)/100)))
        csv_hilo=threading.Thread(name="hilo_csv",target= Descarga_pim_doc,args=(hash_archivo,informacion,string_campos))
        csv_hilo.start()
    
        Txt('prueba','Convierte haciendo uso de cloud img.', inicio,datetime.now())    
        inicio= datetime.now() 
        Txt('prueba','Prepara el archivo csv(hilo)', inicio,datetime.now())   
        inicio= datetime.now() 
        csv_hilo.join()
        Txt('prueba','Queda listo el csv', inicio,datetime.now())
        Txt('prueba','FIN', datetime.now(),datetime.now())
       
        return render(
            request,
            'visualizacion.html',
            {"headers":parametros,
            "lista":informacion,
            "mostrar":'si',
            "token":hash_archivo,
            "rangos":rango,
            "tamano":[largo,ancho]
            })    
        pass
    except Exception as e:
        messages.error(request,'ocurrio un error por favor contacte con el administrador y proporcine este error: {}'.format(e))
        return render(
            request,
            'index.html',
            {'ancho':ancho,
            'largo':largo,
            'tipo':tipo,
            'consulta':parametros,
            'mostrar':'no',
            'marcas':marcas,                      
            "generos":genero,
            "grupo_destinos":grupo_Destino,
            "tipo_prendas":tipo_Prenda})
      
def Consulta_Where_Cantidad(marca,genero,grupo_destino,tipo_prenda):
        count=0
        if (marca!=''):
            count=count+1
        if (genero!=''):
            count=count+1
        if (grupo_destino!=''):
            count=count+1
        if (tipo_prenda!=''):
            count=count+1
        return count
 

def Consulta_Where(marca,genero,grupo_destino,tipo_prenda):   
    var_where=''
    if marca!='':
        var_where = "MARCA='{}'".format(marca)
        pass
    
    if marca=='' and genero!='' :
        var_where="GENERO='{}'".format(genero)
        pass
    elif genero!='' :
        var_where=var_where+"AND GENERO='{}'".format(genero)
        pass

    if  marca=='' and genero=='' and grupo_destino!='':
        var_where="GRUPO_DESTINO='{}'".format(grupo_destino)
        pass
    elif grupo_destino!='':
        var_where=var_where+"AND GRUPO_DESTINO='{}'".format(grupo_destino)
    
    if marca=='' and genero=='' and grupo_destino=='' and tipo_prenda!='':
        var_where="TIPO_PRENDA='{}'".format(tipo_prenda)
        pass
    elif tipo_prenda !='':
        var_where=var_where+"AND TIPO_PRENDA='{}'".format(tipo_prenda)
        pass

    return var_where
    

def Catalogoh(request):
    try: 
        mi_archivo=request.FILES["archivo"]     
        files = mi_archivo.read().decode('utf-8-sig')   
        reader = csv.DictReader(io.StringIO(files),fieldnames=None,delimiter=';')
        archivo = [line for line in reader]                
        #insertamos temporamente datos en una tabla para despues traerlos ordenados de una manera mas sencilla
        carga_temp=[line for line in archivo]    
        Catalogo_temp.objects.all().delete()
        for dato in carga_temp:        
            Catalogo_temp.objects.create(
                material=dato['Material'],
                unidad_empaque=dato['Unidad de empaque'],
                coleccion=dato['Colección'],
                precio=dato['Precio'],
                moneda='',
                pais=dato['Orden'])
        
        header_consulta_material=[]
        for valor in archivo:
            header_consulta_material.append(valor['Material'])
            pass               

        """ 26 px de diferencia en la tercera marca """
        datosGEF=Consulta_marca_catalogo('GEF')
        datosBF=Consulta_marca_catalogo('BABY FRESH')
        datosPB=Consulta_marca_catalogo('PUNTO BLANCO')
        
        can_marca=np.asarray(consultasql("SELECT COUNT(MARCA) AS CANTIDAD,MARCA FROM RAM.CATALOGO GROUP BY MARCA order by MARCA"))
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
                
        return render(
            request,'catalogo.html',
            {'datosGEF' : datosGEF,
            'datosPB' : datosPB,
            'datosBF' : datosBF,
            'Cgef':'height:{}px;'.format(gefh),
            'CPb':'height:{}px;'.format(pbh),
            'Cbf':'height:{}px;'.format(bfh),
            'moneda':dato['Moneda'],
            'logo_gef':Claves.get_secret('LOGO_GEF'),
            'logo_pb':Claves.get_secret('LOGO_PB'),
            'logo_bf':Claves.get_secret('LOGO_BF')})
    except Exception as e:            
        if type(e) is KeyError:
            messages.error(request,'Recuerde que debe de conservar la estructura del archivo plano y este debe de estar separado por ;, error cerca a {}.'.format(e))   
        elif "PRIMARY" in str(e):
            messages.error(request,'Hay un material duplicado, recuerde que deben ser únicos.')
        elif "utf-8" in str(e):
            messages.error(request,'El archivo debe de ser un csv utf-8.')
        else:
            messages.error(request,'Ocurrio un error inesperado, por favor contacte con el administrador y proporcione este error; {}'.format(e))         
            
        return render(request,'index.html',{'mostrar':'no'})  
   
def handler404_page(request):
    return render(request, '404.html', status=404)
    
def Descarga_pim_doc(token,mat,headers):    
    response=csv_pim(token,mat,headers)
    print(response.Guardar())

    

def Descarga_doc(request):    
       
    token = request.POST["token"]
    archivo_csv=open(settings.MEDIA_ROOT+"/Csv_descarga/documento-{}.csv".format(token),'rb')
    return FileResponse(archivo_csv)

def Descarga_img(request):    
    token = request.POST["token"]
    tamanio = [t for t in request.POST["tamano"]] 
    descarga=Descarga_imagenes()
    pru=pd.read_csv(settings.MEDIA_ROOT+"/Csv_descarga/documento-{}.csv".format(token),sep='\n',delimiter=';')
        
    necesario=pru[["ean", "imagen_grande"]]
    necesario=necesario[int(request.POST["rango"])*100:(int(request.POST["rango"])+1)*100]
    lista=necesario.values.tolist()
    largo,ancho=request.POST["tamano"].split(',')      
    temp=descarga.descargar(lista,token,request.POST["rango"],largo,ancho) 
    return temp
        
def Consulta_marca_catalogo(marca):        
    consulta=("SELECT * FROM CATALOGO WHERE MARCA='{}' ORDER BY MARCA,cast(PAIS as unsigned)").format(marca)
    datos=consultasql(consulta)
    consulta_temp=[]
    
    for dato in datos:
        temp=list(dato)        
        colores=MysqlColores.objects.filter(material=dato[1]).values('icono_color')
        if colores:
            temp[11]=[a for a in colores]
        consulta_temp.append(temp)        
    datos=consulta_temp
    datos=cloud.convertir_matriz(
        datos,8,
            248,
            326,
            'aatdtkgdoo')
    return datos



def Validacion(lista,tipo):        
    try:        
        if lista:
            if len(lista[0].keys())>1:
                return('Recuerde que solo puede ingresar una lista de eans o materiales, la que tiene actualmente tiene mas de 1 columna')
            else:
                keys=[]
                for li in lista[0]:
                    keys.append(li)
                    pass 
                con=Converts()
               
                llave=con.convert_array_string(keys,"",",")                   
                if(tipo not in  llave.upper()):
                    return('Usted seleciono un header {} y ingreso un archivo con header {}, por favor valide.').format(tipo,llave)
                else:
                    return (False)
        else:
            return('El documento esta vacio por favor valide')
        pass
    except Exception as e:
        if 'TemporaryUploadedFile' in str(e):
            return 'Se cargo un archivo no valido'
        else:
            return 'Ocurrio un error por favor valide el archivo que se subio, si el error persiste contacte con el administrador y dispoga este error: {}'.format(e)


def consultasql(sql):
    try:        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            mat=cursor.fetchall()
            pass
        return mat
    except Exception as e:        
       return 'Ocurrio un error, por favor contacte con el administrador y brinde este mensaje: {}.'.format(e)   
        
        
    

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
