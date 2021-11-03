from decimal import Context
import pdb
from django.db.models.expressions import OrderBy
from django.shortcuts import render,redirect
from .models import Materiales,Descarga,Catalogo_temp,MysqlColores,Marca,Genero,Grupo_Destino,Tipo_Prenda,MysqlRegistro_Peticiones
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
import xlrd
import openpyxl
from os import path
from os import remove
from django.contrib.auth import get_user_model,authenticate,login as dj_login,logout
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework_simplejwt import authentication
from django.contrib.auth.decorators import login_required,permission_required
from .decorators import unauthenticated_user,allowed_users
from rest_framework import generics
from .task import descarga_asin
# from django.core.context_processors import csrf
from django.template import RequestContext, context
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
# from django.shortcuts import render_to_response
from django.views.decorators.csrf import requires_csrf_token
from datetime import date
# from django.contrib.sites.models import Site

converts_helper=Converts()
cloud=CloudImage()
@login_required(login_url='/')
@csrf_protect
class loginview(APIView):
    # @unauthenticated_user
    def login(request):
        # import pdb; pdb.set_trace()
        if request.user.is_authenticated:
            # Limpiar.limpiar_media_imagenes()
            marcas=Marca.objects.all()        
            genero=Genero.objects.all()
            grupo_Destino=Grupo_Destino.objects.all()
            tipo_Prenda=Tipo_Prenda.objects.all()
            return render(request,
            'index.html', 
            {'marcas':marcas,                      
            "generos":genero,
            "grupo_destinos":grupo_Destino,
            "tipo_prendas":tipo_Prenda,
            "username":request.user}) 
        else:
            username_temp = request.POST.get('username')
            password = request.POST.get('password')
            if username_temp is None or password is None:
                messages.error(request,'No tiene acceso, por favor iniciar sesión.')
                return render(request,'login.html') 
            else:
                User = get_user_model()
                usuario = User.objects.filter(username = username_temp).first()
                if usuario is None :
                    messages.error(request,'El usuario que ingreso no esta registrado.')
                    return render(request,'login.html')   
                elif not usuario.check_password(password):
                    messages.error(request,'Ingreso una contraseña incorrecta.')
                    return render(request,'login.html')   
                else:
                    # Limpiar.limpiar_media_imagenes()
                    marcas=Marca.objects.all()        
                    genero=Genero.objects.all()
                    grupo_Destino=Grupo_Destino.objects.all()
                    tipo_Prenda=Tipo_Prenda.objects.all()
                    dj_login (request, usuario)
                    return render(request,
                            'index.html', 
                            {'marcas':marcas,                      
                            "generos":genero,
                            "grupo_destinos":grupo_Destino,
                            "tipo_prendas":tipo_Prenda,
                            "username":username_temp}) 

@login_required(login_url='/')
def subida(request):
    try:
        if request.user.is_authenticated:        
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
                'URL_IMAGEN',
                'INSTRUCCIONES_LAVADO',
                'CODIGO_COLOR'
                ]
    
            parametros=[]       

            #Capturamos la informacion del formulario          
            tipo = request.POST["tipo"]
            ancho = request.POST["ancho"]
            largo = request.POST["largo"]
            nombre_imagen = request.POST["Nombre_Imagen"] 
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
                    file = file.upper()
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
                eanes_faltantes = Buscar_Eanes_Faltantes(string_filtro,matconsulta,string_campos)
            elif request.POST['Ean_Consul']!= "":
                array_filt=converts_helper.convert_string_array(ean_consulta)
                string_filtro_ean=converts_helper.convert_array_str(array_filt,',',False)
                consulta='select distinct {} from material_materiales where ean in ({});'.format(string_campos,string_filtro_ean) 
                matconsulta=consultasql(consulta)
                eanes_faltantes = Buscar_Eanes_Faltantes(array_filt,matconsulta,string_campos)
                

            else:
                consulta='select distinct {} from material_materiales where {};'.format(string_campos,Consulta_Where(request.POST['DWMarca'],request.POST['DWGenero'],request.POST['DWGrupo_destino'],request.POST['DWTipo_prenda']))
                matconsulta=consultasql(consulta)    


    

                    
            Txt('prueba','Realiza la consulta en la base de datos', inicio,datetime.now())
            inicio= datetime.now()        
                
            #converitmos todo haciendo uso de cloud img  
            tipo_consulta='documento'
            informacion=cloud.convertir_matriz(
                matconsulta,
                1,
                ancho,
                largo,
                Claves.get_secret('CLOUDIMG_TOKEN'),
                tipo_consulta)      
            hash_archivo = str(uuid.uuid1())
            Txt('prueba','Resizen cloud img', inicio,datetime.now())
            inicio= datetime.now()         
            rango=list(range(0,ceil(len(informacion)/100)))
            # import pdb; pdb.set_trace()
            df = pd.DataFrame(eanes_faltantes,columns=['ean'])
            df_list = df.to_numpy().tolist()
            cantidad_datos = df.count()
            cantidad_datos = int(cantidad_datos)
            csv_hilo_ean = threading.Thread(name="hilo_csv",target= Descarga_Ean_Faltantes_doc,args=(hash_archivo,df_list,'ean'))
            csv_hilo_ean.start()
            csv_hilo=threading.Thread(name="hilo_csv",target= Descarga_pim_doc,args=(hash_archivo,informacion,string_campos))
            csv_hilo.start()
        
            Txt('prueba','Convierte haciendo uso de cloud img.', inicio,datetime.now())    
            inicio= datetime.now() 
            Txt('prueba','Prepara el archivo csv(hilo)', inicio,datetime.now())   
            inicio= datetime.now()
            csv_hilo_ean.join() 
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
                "nombre": nombre_imagen,
                "cantidad": cantidad_datos,
                "tamano":[largo,ancho]
                })    
            pass
    except Exception as e:
        if 'NoneType' in str(e):
            messages.error(request,f'Por favor valide que el encabezado sea {tipo}')
        else: 
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

@login_required(login_url='/')
def carga(request):
    try:
        if request.user.is_authenticated:     
            inicio= datetime.now()  
            marcas=Marca.objects.all()        
            genero=Genero.objects.all()
            grupo_Destino=Grupo_Destino.objects.all()
            tipo_Prenda=Tipo_Prenda.objects.all()
            Txt('prueba','INICIO', datetime.now(),datetime.now())
            inicio= datetime.now()   
            consulta=[
                'MATERIAL',
                'EAN',
                'URL_IMAGEN'
                ]
    
            parametros=[]       
            #Capturamos la informacion del formulario       
            tipo = request.POST["tipo"]
            ean_consulta = request.POST["Ean_Consulta"]  
            tipo_genero = request.POST.getlist("DWGenero")
            tipo_marca = request.POST.getlist("DWMarca")
            marca_planeacion = converts_helper.convert_array_str_consulta(tipo_marca,',',False)
            genero_planeacion = converts_helper.convert_array_str_consulta(tipo_genero,',',False)
            
            if len(request.FILES)!=0 and tipo =='':
                messages.error(request,'Por favor seleccione el medio de consulta.')
                return render(
                    request,
                    'index.html',
                    {'tipo':tipo,
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
                                {'tipo':tipo,
                                'consulta':parametros,
                                'mostrar':'no',
                                'marcas':marcas,                      
                                "generos":genero,
                                "grupo_destinos":grupo_Destino,
                                "tipo_prendas":tipo_Prenda
                                })

            
            if len(request.FILES)==0:
                count=0
                if (len(tipo_marca)!=0):
                    count=count+1
                if (len(tipo_genero)!=0):
                    count=count+1
                if (request.POST['DWGrupo_destino']!=''):
                    count=count+1
                if (request.POST['DWTipo_prenda']!=''):
                    count=count+1
                if(request.POST['Ean_Consulta']!=''):
                    count=count+1
                
                if len(tipo_marca)!=0 or len(tipo_genero)!=0 or request.POST['DWGrupo_destino']!='' or request.POST['DWTipo_prenda']!='' :
                    if request.POST['Ean_Consulta']!= '':
                        messages.error(request,'Por favor verifique como desea hacer la consulta si por ean o selección.')
                        return render(
                            request,
                            'index.html',
                            {'tipo':tipo,
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
                        {'tipo':tipo,
                        'consulta':parametros,
                        'mostrar':'no',
                        'marcas':marcas,                      
                        "generos":genero,
                        "grupo_destinos":grupo_Destino,
                        "tipo_prendas":tipo_Prenda})

            
        
        
            string_campos=converts_helper.convert_array_string(parametros,tipo,",") #nos permite traer un string de campos a partir de un arreglo
            if string_campos=='':
                string_campos='material,ean,url_imagen'
                parametros=['MATERIAL','EAN','URL_IMAGEN']   
                pass
            else:
                parametros=['MATERIAL','EAN','URL_IMAGEN']+parametros 
                string_campos='material,ean,url_imagen,'+string_campos
            Txt('prueba','Valida informacion e inicializa campos.', inicio,datetime.now())    
            inicio= datetime.now() 
            if len(request.FILES)!=0 and request.POST["Ean_Consulta"]== '' :   # si carga un archivo entra aqui         
                mi_archivo=request.FILES["archivo_Con"]            
                try:
                    file = mi_archivo.read().decode('utf-8-sig')
                    file = file.upper()
                    reader = csv.DictReader(io.StringIO(file))                  
                    archivo = [line for line in reader]    
                
                except Exception as e:
                    messages.error(request,"Por favor valide bien la estructura del archivo, si el error persiste contacte con el administrador. y disponga este error:{}".format(e))
                    return render(
                    request,
                    'index.html',
                    {'tipo':tipo,
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
                    {'tipo':tipo,
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
            elif request.POST['Ean_Consulta']!= "":
                array_filt=converts_helper.convert_string_array(ean_consulta)
                string_filtro_ean=converts_helper.convert_array_str(array_filt,',',False)
                consulta='select distinct {} from material_materiales where ean in ({});'.format(string_campos,string_filtro_ean) 
                matconsulta=consultasql(consulta)
                # import pdb; pdb.set_trace()

            else:
                consulta='select distinct {} from material_materiales where {};'.format(string_campos,Consulta_Where_Planeacion(marca_planeacion,genero_planeacion,request.POST['DWGrupo_destino'],request.POST['DWTipo_prenda']))
                matconsulta=consultasql(consulta)    


    

                    
            Txt('prueba','Realiza la consulta en la base de datos', inicio,datetime.now())
            inicio= datetime.now()        
                        
            hash_archivo = str(uuid.uuid1())
            Txt('prueba','Resizen cloud img', inicio,datetime.now())
            inicio= datetime.now()         
            csv_hilo=threading.Thread(name="hilo_csv",target= Descarga_pim_doc,args=(hash_archivo,matconsulta,string_campos,1))
            csv_hilo.start()
        
            Txt('prueba','Convierte haciendo uso de cloud img.', inicio,datetime.now())    
            inicio= datetime.now() 
            Txt('prueba','Prepara el archivo csv(hilo)', inicio,datetime.now())   
            inicio= datetime.now() 
            csv_hilo.join()
            Txt('prueba','Queda listo el csv', inicio,datetime.now())
            Txt('prueba','FIN', datetime.now(),datetime.now())

            parametros=['MATERIAL','EAN','URL FRONT']
            matconsulta = pd.DataFrame(matconsulta)
            matconsulta_reducida = matconsulta.head(100)
            resultado = len(matconsulta) - len(matconsulta_reducida)
            matconsulta = matconsulta_reducida.to_numpy().tolist()
            estado_mensaje = 0

            return render(
                request,
                'visualizacion.html',
                {"headers":parametros,
                "lista":matconsulta,
                "mostrar":'si',
                "token":hash_archivo,
                "estado": estado_mensaje,
                "faltantes": int(resultado)
                })    
            pass
    except Exception as e:
        if 'NoneType' in str(e):
            messages.error(request,f'Por favor valide que el encabezado sea {tipo}')
        else: 
            messages.error(request,'ocurrio un error por favor contacte con el administrador y proporcine este error: {}'.format(e))
        return render(
            request,
            'index.html',
            {'tipo':tipo,
            'consulta':parametros,
            'mostrar':'no',
            'marcas':marcas,                      
            "generos":genero,
            "grupo_destinos":grupo_Destino,
            "tipo_prendas":tipo_Prenda})


def Buscar_Eanes_Faltantes(ean_iniciales, ean_encontrados,campos):
    
    df_ean_buscar = pd.DataFrame(ean_iniciales,columns=['ean'])
    lista_campos = campos.split(",")
    df_ean_encontrados = pd.DataFrame(ean_encontrados, columns = lista_campos)
    df_ean_encontrados['eans2'] = df_ean_encontrados['ean']
    eanes_faltantes = pd.merge(df_ean_buscar, df_ean_encontrados, on='ean', how='left')
    eanes_faltantes = eanes_faltantes[eanes_faltantes.eans2.isnull()]
    eanes_faltantes = eanes_faltantes['ean']
    return eanes_faltantes

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
    
def Consulta_Where_Planeacion(marca,genero,grupo_destino,tipo_prenda):
    var_where=''
    if marca!='':
        var_where = "MARCA in ({})".format(marca)
        pass
    
    if marca=='' and genero!='' :
        var_where="GENERO in ({})".format(genero)
        pass
    elif genero!='' :
        var_where=var_where+" AND GENERO in ({})".format(genero)
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

@login_required(login_url='/')
def Catalogog(request):

    try:
        if request.user.is_authenticated:
            if request.method == "POST":
                mi_archivo = request.FILES["archivo_excel"]
                if mi_archivo.name.endswith('xlsx'):
                    id = str(uuid.uuid1())
                    ruta = settings.MEDIA_ROOT + '/Upload/' + mi_archivo.name
                    with open (ruta,'wb+') as destination: 
                            for chunk in mi_archivo.chunks():
                                destination.write(chunk)
                    os.rename(settings.MEDIA_ROOT + '/Upload/' + mi_archivo.name, settings.MEDIA_ROOT + '/Upload/' + "{}.xlsx".format(id)) 
                    open_files=pd.ExcelFile(settings.MEDIA_ROOT + '/Upload/' + '{}.xlsx'.format(id))
                    titulo_files = request.POST["nombre_hoja"]
                    titulo = titulo_files
                    titulos = open_files.sheet_names
                    lista_titulos = [line for line in titulos]
                    # print(lista_titulos)
                    if titulo in lista_titulos:
                        df = pd.read_excel(open_files,sheet_name = titulo)
                        df_1= df[['Material','Unidad de empaque', 'Colección','Precio','Moneda','Orden']]
                        df_2 = df_1.dropna(subset=["Material"])
                        df_2 = df_2.astype({"Material": int, "Unidad de empaque": int,"Precio":int,"Orden": int})
                        # print(df_2)
                        temp = [ row for index, row in df_2.iterrows()]
                        archivo_temp = [line for line in  temp]
                        #insertamos temporalmente datos en una tabla para despues traerlos ordenados de una manera mas sencilla
                        carga_temp=[line for line in archivo_temp]                         
                    
                        for dato in carga_temp:        
                            Catalogo_temp.objects.create(
                                material=dato['Material'],
                                unidad_empaque=dato['Unidad de empaque'],
                                coleccion=dato['Colección'],
                                precio=dato['Precio'],
                                moneda='',
                                pais=dato['Orden'],
                                hash_uuid=id
                                )
                        # moneda_temp = dato['Moneda']
                        header_consulta_material=[]
                        for valor in temp:
                            header_consulta_material.append(valor['Material'])
                            pass               

                        """ 10 px de diferencia en la tercera marca """
                        datosGEF=Consulta_marca_catalogo('GEF',id)
                        datosBF=Consulta_marca_catalogo('BABY FRESH',id)
                        datosPB=Consulta_marca_catalogo('PUNTO BLANCO',id)
                        can_marca=np.asarray(consultasql("SELECT COUNT(MARCA) AS CANTIDAD,MARCA FROM CATALOGO WHERE HASH_UUID='{}'  GROUP BY MARCA order by MARCA".format(id)))
                        con=0
                        bfh=0# hojas Baby fresh
                        pbh=0#hojas Punto blanco
                        gefh=0#hojas gef
                        cantidad_marcas=consultasql("SELECT COUNT(*) FROM ( SELECT COUNT(MARCA) AS CANTIDAD,MARCA FROM RAM.CATALOGO WHERE HASH_UUID='{}' GROUP BY MARCA order by MARCA) CAM".format(id))
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
                                    gefh=gefh-10
                                
                                pass

                        Catalogo_temp.objects.filter(hash_uuid=id).delete()
                        if path.exists(settings.MEDIA_ROOT + '/Upload/' + '{}.xlsx'.format(id)):
                            open_files.close()
                            remove(settings.MEDIA_ROOT + '/Upload/' + '{}.xlsx'.format(id))
                        else:
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
                else:
                    messages.error(request,'Ingreso el nombre Incorrectamente, por favor vuelva a intentar.')
                    return render(request,'index.html',{'mostrar':'no'})         
            messages.error(request,'Recuerde que el archivo debe ser un excel(.xlsx).')
            return render(request,'index.html',{'mostrar':'no'}) 
        messages.error(request,'Ocurrio un error inesperado, por favor contacte con el administrador y proporcione este error:Es un metodo diferente a post')
        return render(request,'index.html',{'mostrar':'no'}) 

    except Exception as e:
        if type(e) is KeyError:
            messages.error(request,'Recuerde que debe de conservar la estructura del archivo, error cerca a {}.'.format(e))   
        # elif type(e) is ValueError:
        #     messages.error(request,'Recuerde que la estructura del archivo debe ser xlsx.')
        elif "carga_temp" in str(e):
            messages.error(request,'El Nombre de la hoja que desean ingresar no se encuentra en el archivo, por favor valide!!.')
        elif("Duplicate entry" in  str(e)):
            messages.error(request,'Recuerde que debe de conservar la estructura del archivo  y no debe contener duplicados ') 
        else:
            messages.error(request,'Ocurrio un error inesperado, por favor contacte con el administrador y proporcione este error; {}'.format(e))         
            
        return render(request,'index.html',{'mostrar':'no'}) 


def handler404_page(request):
    return render(request, '404.html', status=404)


# @login_required(login_url='/')    
def Descarga_pim_doc(token,mat,headers,planeacion=0):
        
    response=csv_pim(token,mat,headers,planeacion)
    response.Guardar()

def Descarga_Ean_Faltantes_doc(token,mat,headers,planeacion=3):
    response=csv_pim(token,mat,headers,planeacion)
    response.Guardar()

def Descargar_Ean_Faltantes(request):
    token = request.POST["token"]
    archivo_csv = open()
    return FileResponse(archivo_csv)


def Descarga_doc_eanes_faltantes(request):    
       
    token = request.POST["token"]
    # response=csv_pim(token,mat,headers)
    archivo_csv = open(settings.MEDIA_ROOT + "/Csv_descarga/EansNoEncontrados-{}.csv".format(token),'rb')
    return FileResponse(archivo_csv)

def Descarga_doc(request):    
       
    token = request.POST["token"]
    # response=csv_pim(token,mat,headers)
    archivo_csv = open(settings.MEDIA_ROOT + "/Csv_descarga/documento-{}.csv".format(token),'rb')
    return FileResponse(archivo_csv)

# @login_required(login_url='/')
def Descarga_img(request): 
    # import pdb; pdb.set_trace()
    token = request.POST["token"]
    nombre_img = request.POST["nombre"]
    pru=pd.read_csv(settings.MEDIA_ROOT+"/Csv_descarga/documento-{}.csv".format(token),sep='\n',delimiter=';')      
    necesario=pru[["ean", "imagen_grande"]]
    lista=necesario.values.tolist()
    largo,ancho=request.POST["tamano"].split(',')
    # primer registro de la peticion
    query = MysqlRegistro_Peticiones(id=token,fecha_peticion=datetime.now(),estado="Iniciado",usuario=request.user,estado_borrado = 0 )  
    query.save() 
    descarga_asin.delay(lista,token,largo,ancho,nombre_img)
    msj = str(request.user) + " el proceso de descarga se ha iniciado, puede hacerle seguimiento en el siguiente enlace:" 
    messages.success(request,msj,extra_tags="descarga")
    
    marcas=Marca.objects.all()        
    genero=Genero.objects.all()
    grupo_Destino=Grupo_Destino.objects.all()
    tipo_Prenda=Tipo_Prenda.objects.all()
    return render(request,
            'index.html',
            {'marcas':marcas,                      
            "generos":genero,
            "grupo_destinos":grupo_Destino,
            "tipo_prendas":tipo_Prenda}) 
        
def Consulta_marca_catalogo(marca,hash_uuid):       
    consulta=("SELECT * FROM CATALOGO WHERE MARCA='{}' AND HASH_UUID ='{}' ORDER BY MARCA,cast(PAIS as unsigned)").format(marca,hash_uuid)
    datos=consultasql(consulta)
    consulta_temp=[]
    
    for dato in datos:
        temp=list(dato)        
        colores=MysqlColores.objects.filter(material=dato[1]).values('icono_color')
        codigo=MysqlColores.objects.filter(material=dato[1]).values('codigo_color')
        if colores and codigo:
            temp[11]=[a for a in colores]
            temp[13]=[b for b in codigo]
        consulta_temp.append(temp)        
    datos=consulta_temp
    tipo_consul='catalogo'
    datos=cloud.convertir_matriz(
        datos,8,
            248,
            326,
            'agnravsvaq',
            tipo_consul)
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
        elif 'NoneType' in str(e):
            return 'Por favor valide que el archivo diga EAN o MATERIAL, no esta permitido  {}'.format(lista[0].keys())
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

@csrf_protect
class homeview(APIView):
    def home(request):
        if request.user.is_authenticated:
            # Limpiar.limpiar_media_imagenes()
            marcas=Marca.objects.all()        
            genero=Genero.objects.all()
            grupo_Destino=Grupo_Destino.objects.all()
            tipo_Prenda=Tipo_Prenda.objects.all()
            return render(request,
            'index.html', 
            {'marcas':marcas,                      
            "generos":genero,
            "grupo_destinos":grupo_Destino,
            "tipo_prendas":tipo_Prenda,
            "username":request.user})
        else:         
            return render(
            request,
            'login.html')
   
@login_required(login_url='/')
def Consultar_Estado_Tarea(request):
    try:
        # dominio = Site.objects.get_current().domain

        if request.user.is_authenticated:

            query = MysqlRegistro_Peticiones.objects.filter (usuario = request.user).order_by('-fecha_peticion').values()
            # pdb.set_trace()
            parametros = ['ID','INICIADO','TERMINADO','ESTADO','DESCARGAR IMAGENES','DESCARGAR DOCUMENTO','BORRAR PETICIÓN']   
            return render(
            request,
            'portal.html',
            {"titulos":parametros,
            "informacion":query,
            # "url":dominio
            }) 
        else:
            messages.error(request,'No tiene acceso, por favor iniciar sesión.')
            return render(request,'login.html')     
    except Exception as e:        
       return 'Ocurrio un error, por favor contacte con el administrador y brinde este mensaje: {}.'.format(e)


def Descargar_Documento_Peticion(request,id):
    if request.user.is_authenticated:
        query = MysqlRegistro_Peticiones.objects.get(pk=id)
        if query.estado_borrado == 0:
            archivo_csv = open(settings.MEDIA_ROOT + "/Csv_descarga/documento-{}.csv".format(id),'rb')
            return FileResponse(archivo_csv)
    else:
            messages.error(request,'No tiene acceso, por favor iniciar sesión.')
            return render(request,'login.html')         


def Descargar_Imagenes_Peticion(request,id):
    if request.user.is_authenticated:
        query = MysqlRegistro_Peticiones.objects.get(pk=id)
        if query.estado_borrado == 0:
            dire=settings.MEDIA_ROOT+"\Imagenes_descarga" 
            if os.path.isfile(dire + f'\\{id}\\Imagenes-{id}.zip'):
                zip_file = open(dire +f'\\{id}\\Imagenes-{id}.zip', 'rb')
                return FileResponse(zip_file)
    else:
        messages.error(request,'No tiene acceso, por favor iniciar sesión.')
        return render(request,'login.html') 

def Borrar_Peticion(request,id):
    if request.user.is_authenticated:
        query = MysqlRegistro_Peticiones.objects.get(pk=id)
        query.estado_borrado = 1
        query.save()
        return redirect('/portal')
    else:
        messages.error(request,'No tiene acceso, por favor iniciar sesión.')
        return render(request,'login.html') 
        

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
 


