import requests
import csv
from datetime import datetime
from django.db import models
import urllib.request as req
import wget
import os

class Descarga(models.Model):
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 

    def Descargaindividual(self,link,nombre):  
        url = link # El link de la imagen
        
        nombre_local_imagen = nombre+".png" # El nombre con el que queremos guardarla
        try:                                
            myfile = requests.get(url)        
            download_folder = os.path.expanduser("~")+"/Downloads/Descarga_imagenes/"
            os.makedirs(download_folder, exist_ok=True)
            open(download_folder+nombre+'.png', 'wb').write(myfile.content)
                
        except Exception as e:
            return e
            pass
        pass
           
    def descargar(self,imagenes_descarga):
        
        for dir in imagenes_descarga:            
            self.Descargaindividual(dir['imagen_grande'],dir['ean'])               
            pass  
        pass
