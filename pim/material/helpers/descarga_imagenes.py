import requests
import csv
from datetime import datetime
from django.db import models
import urllib.request as req
import wget
import os
from django.http import HttpResponse,FileResponse
from django.conf import settings
import os
import zipfile
from .limpiar import Limpiar
class Descarga_imagenes(models.Model):
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 

    def Descargaindividual(self,link,nombre):  
        url = link # El link de la imagen
        
        nombre_local_imagen = nombre+".png" # El nombre con el que queremos guardarla
        try:                                
            myfile = requests.get(url)
            download_folder = settings.MEDIA_ROOT+"/Imagenes_descarga/"
            filename=download_folder+nombre+'.png'  
            os.makedirs(download_folder, exist_ok=True)
            open(filename, 'wb').write(myfile.content) 
        except Exception as e:
            return e
            pass
        pass
           
    def descargar(self,imagenes_descarga):
        dire=settings.MEDIA_ROOT+"/Imagenes_descarga"
        Limpiar.limpiar_media_imagenes()        
        for dir in imagenes_descarga:            
            if 'None' not in dir:
                self.Descargaindividual(dir['imagen_grande'],dir['ean'])
            pass 
        fantasy_zip = zipfile.ZipFile(dire+'\\archive.zip', 'w')
        for folder, subfolders, files in os.walk(dire):        
            for file in files:
                if file.endswith('.png'):
                    fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), dire+file), compress_type = zipfile.ZIP_DEFLATED) 
                    os.remove(folder+'/'+file)                     
        
        fantasy_zip.close()
        zip_file = open(dire+'\\archive.zip', 'rb')            
        return FileResponse(zip_file)
               


    