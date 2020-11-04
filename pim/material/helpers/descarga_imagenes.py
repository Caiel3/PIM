import requests
import csv
from datetime import datetime
import urllib.request as req
import wget
import os
from django.http import HttpResponse,FileResponse
from django.conf import settings
import os
import zipfile
from .limpiar import Limpiar
from datetime import datetime
from ..helpers.TxtControlador import Txt

class Descarga_imagenes():
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 

    def Descargaindividual(self,link,nombre,token):  
        
        nombre=str(nombre)
        url = link # El link de la imagen
        
        nombre_local_imagen = nombre+".jpg" # El nombre con el que queremos guardarla
        try:                                
            myfile = requests.get(url)
            download_folder = settings.MEDIA_ROOT+"/Imagenes_descarga/{}/".format(token)
            filename=download_folder+nombre+'.jpg'  
            os.makedirs(download_folder, exist_ok=True)
            open(filename, 'wb').write(myfile.content) 
        except Exception as e:
            return e
            pass
        pass
           
    def descargar(self,imagenes_descarga,token):           
        inicio= datetime.now() 
        import pdb;pdb.set_trace()           
        dire=settings.MEDIA_ROOT+"/Imagenes_descarga"        
        if os.path.isdir(dire+'/{}'.format(token))== False:
            os.mkdir(dire+'/{}'.format(token))
            pass        
        dire=settings.MEDIA_ROOT+"/Imagenes_descarga/{}".format(token)
        archivo='Imagenes-{}'.format(token)          
        for dir in imagenes_descarga:            
            if ''!=dir:
                self.Descargaindividual(dir[1],dir[0]+'-FRENTE',token) if dir[1] != None else ''
                self.Descargaindividual(dir[2],dir[0]+'-ESPALDA',token) if dir[2] != None else ''
                self.Descargaindividual(dir[3],dir[0]+'-DETALLE',token) if dir[3] != None else ''
                self.Descargaindividual(dir[4],dir[0]+'-DETALLE2',token) if dir[4] != None else ''
                self.Descargaindividual(dir[5],dir[0]+'-MODELO',token) if dir[5] != None else ''
            pass 
        Txt('prueba','Realiza la descarga de imagenes.', inicio,datetime.now())
        inicio= datetime.now()    
        fantasy_zip = zipfile.ZipFile(dire+'\\{}.zip'.format(archivo), 'w')
        for folder, subfolders, files in os.walk(dire):        
            for file in files:
                if file.endswith('.jpg'):
                    fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), dire+file), compress_type = zipfile.ZIP_DEFLATED) 
                    os.remove(folder+'/'+file)                     
        
        fantasy_zip.close()
        zip_file = open(dire+'\\{}.zip'.format(archivo), 'rb') 
        Txt('prueba','Crea el zip para descargar.', inicio,datetime.now())           
        return FileResponse(zip_file)
               


    