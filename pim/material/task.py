from celery import shared_task
from pim.celery import app
from .helpers.descarga_imagenes import Descarga_imagenes
from .models import MysqlRegistro_Peticiones
from datetime import datetime

# from celery.contrib import rdb
import time 
import os

@app.task
# @shared_task
def descarga_asin(lista_temp,token,largo,ancho):
    # print(str(lista_temp))
    # open("d:\\datos.txt", "w+")
    # update va ontener la fecha inicio
    query = MysqlRegistro_Peticiones.objects.get(pk=token)
    query.fecha_inicio = datetime.now()
    query.save()
    # rdb.set_trace()
    descarga_img=Descarga_imagenes()
    temp = descarga_img.descargar(lista_temp,token,largo,ancho)
    # for x in temp:
    #     print('ImagenI')
    #     print(x)
    #     time.sleep(20)
    #     print('ImagenF')
    #segundo registto    
    return temp

