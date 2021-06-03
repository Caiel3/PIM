from celery import shared_task
from pim.celery import app
from .helpers.descarga_imagenes import Descarga_imagenes
import time 
import os

@app.task
# @shared_task
def descarga_asin(lista_temp,token,largo,ancho):
    # print(str(lista_temp))
    # open("d:\\datos.txt", "w+")
    descarga=Descarga_imagenes()
    temp = descarga.descargar(lista_temp,token,largo,ancho)
    # for x in temp:
    #     print('ImagenI')
    #     print(x)
    #     time.sleep(20)
    #     print('ImagenF')
    return temp

