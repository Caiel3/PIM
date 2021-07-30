import requests
import csv
from datetime import datetime
import urllib.request as req
from requests.api import request
import wget
import os
from django.http import HttpResponse,FileResponse
from django.conf import settings
import os,os.path
import zipfile
from .limpiar import Limpiar
from datetime import datetime
from ..helpers.TxtControlador import Txt
from ..models import MysqlImagenes,MysqlRegistro_Peticiones,User
from ..helpers.claves import  Claves
from ..helpers.CloudImage import  CloudImage
from datetime import datetime
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail import get_connection
from django.template.loader import render_to_string
from django.shortcuts import render
# from celery.contrib import rdb
class Descarga_imagenes():
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 

    def Descargaindividual(self,link,nombre,token):  
        # rdb.set_trace()
        nombre=str(nombre)
        url = link # El link de la imagen
        
        nombre_local_imagen = nombre+".jpg" # El nombre con el que queremos guardarla
        try:                                
            myfile = requests.get(url)
            download_folder = settings.MEDIA_ROOT+"\Imagenes_descarga\{}\\".format(token)
            filename=download_folder+nombre+'.jpg'  
            os.makedirs(download_folder, exist_ok=True)
            open(filename, 'wb').write(myfile.content) 
        except Exception as e:
            return e
            pass
        pass
           
    def descargar(self,imagenes_descarga,token,largo,ancho):    
        # rdb.set_trace()      
        inicio= datetime.now() 
    
        dire=settings.MEDIA_ROOT+"\Imagenes_descarga"        
        if os.path.isdir(dire+'\{}'.format(token))== False:
            os.mkdir(dire+'\{}'.format(token))
            pass        
        dire=settings.MEDIA_ROOT+"\Imagenes_descarga\{}".format(token)        
        archivo='Imagenes-{}'.format(token)          
        if os.path.isfile(dire+'\\{}.zip'.format(archivo)):
            zip_file = open(dire+'\\{}.zip'.format(archivo), 'rb')
            # return FileResponse(zip_file)
            pass
        for dir in imagenes_descarga:            
            if ''!=dir:
                consulta_temp=MysqlImagenes.objects.values('ean','imagen').filter(ean=dir[0])
                count=0            
                for img in consulta_temp:                 
                    self.Descargaindividual(
                        link= CloudImage.cloudimg_imagen('',img['imagen'],{"height":largo,"width":ancho},Claves.get_secret('CLOUDIMG_TOKEN'),'documento')
                        ,nombre= str(img['ean'])+'-'+str(count)
                        ,token= token) if img['imagen'] != None else ''
                    count=count+1              
            pass 
        Txt('prueba','Realiza la descarga de imagenes.', inicio,datetime.now())
        inicio= datetime.now()    
        fantasy_zip = zipfile.ZipFile(dire+'\\{}.zip'.format(archivo), 'w')
        for folder, subfolders, files in os.walk(dire):        
            for file in files:
                if file.endswith('.jpg'):
                    fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), dire+file), compress_type = zipfile.ZIP_DEFLATED) 
                    os.remove(folder+'\\'+file)                     
        fantasy_zip.close()
        query = MysqlRegistro_Peticiones.objects.get( pk=token)
        query.fecha_terminado = datetime.now()
        query.estado = 'Terminado'
        query.save()
        query_user= User.objects.get(username=query.usuario)
        # query_2 = User.objects.get( pk=query.usuario)
        # Envio de Correo 
        asunto = "Notificación Petición Terminada"
        mensajeCorreo= render_to_string(
            'asunto.html',{
                'fecha':query.fecha_peticion,
                'url_portal':settings.URL_PORTAL
            },
        )
        # asunto,cuerpo,quien lo envia, quien recibe 
        msg = EmailMessage(asunto,mensajeCorreo,settings.EMAIL_HOST_USER,[query_user.email]) 
        # send_mail(asunto,mensajeCorreo,settings.EMAIL_HOST_USER,['pruebaspim2021@gmail.com'],fail_silently=False)
        msg.content_subtype="html"
        msg.send()
        # zip_file = open(dire+'\\{}.zip'.format(archivo), 'rb') 
        #update termino
        Txt('prueba','Crea el zip para descargar.', inicio,datetime.now())           
        # return FileResponse(zip_file)
               


    