from django.conf import settings
import os.path as path
import numpy as np
from ..helpers.converts import  Converts
from datetime import datetime
from ..helpers.TxtControlador import Txt
from django.contrib.auth.decorators import login_required


class csv_pim:
    def __str__(self):
        return 

    def __unicode__(self):
        return 


    def __init__(self, hash, matriz,headers,planeacion):
      self.hash = hash
      self.matriz = matriz
      self.headers=headers
      self.planeacion=planeacion
    

    def Guardar(self):        
        inicio=datetime.now()             
        ruta=settings.MEDIA_ROOT+'/Csv_descarga/documento-{}.csv'.format(self.hash)
        # import pdb; pdb.set_trace()
        with open(ruta,'a', encoding='UTF-8') as f:
            if self.planeacion == 1:
                f.write(self.headers.replace(',',';').replace('url_imagen','url front')+ '\n')
            else:
                f.write(self.headers.replace(',',';') + '\n')
            for item in self.matriz:
                string_campos=Converts.convert_array_string(self,item,'',';',True)
                if string_campos:
                    f.write(string_campos + '\n')
                # import pdb; pdb.set_trace()  
        f.close()
        Txt('prueba','Crea el csv.', inicio,datetime.now())
        
        return ruta

    