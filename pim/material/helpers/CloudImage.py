import requests
import json
import numpy as np

class CloudImage(object):
    
     

    def __init__(self, token):                
        global gtoken        
        gtoken=token
        pass

       
    def cloudimg_imagen(self,url,parametros):
        parametros_url=''
        for param in parametros:
            parametros_url=str(parametros_url)+"&"+str(param)+'='+str(parametros.get(param))
            pass
                  
        return "https://{}.cloudimg.io/v7/{}?sharp=1{}".format(gtoken,url,parametros_url)

    def inactivar_Imagenes(self,urls):
        url=urls
        respuesta=requests.get(url)
        print(respuesta)
        pass
       
    def regla_json(self,texto):
        with open('Reglas.json','r') as r:
            reglas=json.load(r)
            regla=reglas.get(texto)
        return regla
        pass

    def convertir_matriz(self,matriz,columna,ancho,largo):            
        aux=np.asarray(matriz)    
        con_filas=0        
        try:
            while con_filas<len(aux):
                val=self.cloudimg_imagen(aux[con_filas][columna],{"width":ancho,"height":largo})   
                aux[con_filas,columna]=  val
                con_filas=con_filas+1       
                pass
            pass
        except Exception as e:
            print(e)
            pass
            
        return aux



 



#i=img.cloudimg_imagen(
 #   'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Albert_Einstein_Head.jpg/450px-Albert_Einstein_Head.jpg'
  #  ,{"width":1200,"height":800}
   # )



#inac=CloudImage('','')
#inac.inactivar_Imagenes('https://api.cloudimage.com/invalidate')
