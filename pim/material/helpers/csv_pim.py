from django.conf import settings
import os.path as path
import numpy as np
from ..helpers.converts import  Converts
class csv_pim:
    def __str__(self):
        return 

    def __unicode__(self):
        return 


    def __init__(self, hash, matriz,headers):
      self.hash = hash
      self.matriz = matriz
      self.headers=headers
    

    def Guardar(self):
        inicio=datetime.now()             
        ruta=settings.MEDIA_ROOT+'/Csv_descarga/documento-{}.csv'.format(self.hash)        
        with open(ruta,'a', encoding='UTF-8') as f:
            f.write(self.headers.replace(',',';')+'\n')
            for item in self.matriz:
                
                string_campos=Converts.convert_array_string(self,item,'',';',True)
                f.write(string_campos+'\n')
             
        f.close()
        Txt('prueba','Crea el csv.', inicio,datetime.now())
        
        return ruta

    