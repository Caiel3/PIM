import json
import numpy as np
from django.db import models
     
   

class CloudImage(models.Model):
    
    
    def __str__(self):
        
        return 

    def __unicode__(self):
        return 

    def cloudimg_imagen(self,url,parametros,toquen):
        parametros_url=''
        for param in parametros:
            parametros_url=str(parametros_url)+"&"+str(param)+'='+str(parametros.get(param))
            pass
                  
        return "https://{}.cloudimg.io/v7/{}?sharp=1{}".format(toquen,url,parametros_url)



    def convertir_matriz(self,matriz,headers,ancho,largo,token):         
        aux=matriz        
        headeraux=np.asarray(headers)        
        auxreturn=[]
        con_filas=0      
        posicioni=0
        if 'IMAGEN_GRANDE' in headeraux:
            posicion=np.where(headeraux=='IMAGEN_GRANDE')
            posicioni=posicion[0]
            pass
        else:
            return matriz
        try:
            while con_filas<len(aux):
                for fila in aux:                   
                    url=str(fila[posicioni[0]])
                    if 'None' in url:  
                        val=''
                    else:                          
                        val=self.cloudimg_imagen(url,{"width":ancho,"height":largo},token)
                    lista=list(fila)                    
                    lista[posicioni[0]]=val
                    con_filas=con_filas+1    
                    auxreturn.append(lista)                                                 
                pass
            pass           
        except Exception as e:
            print(e)
            pass
            
        return auxreturn
 



#i=img.cloudimg_imagen(
 #   'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Albert_Einstein_Head.jpg/450px-Albert_Einstein_Head.jpg'
  #  ,{"width":1200,"height":800}
   # )



#inac=CloudImage('','')
#inac.inactivar_Imagenes('https://api.cloudimage.com/invalidate')
