import json
import numpy as np

     
   

class CloudImage():
    
    
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



    def convertir_matriz(self,matriz,posicion,ancho,largo,token):         
        aux=matriz                
        auxreturn=[]
        con_filas=0              
        try:
            while con_filas<len(aux):
                for fila in aux:                   
                    if posicion=='full' :
                        val=self.cloudimg_imagen(fila[1],{"height":largo,"width":ancho},token) if fila[1] != None else ''
                        val1=self.cloudimg_imagen(fila[2],{"height":largo,"width":ancho},token) if fila[2] != None else ''
                        val2=self.cloudimg_imagen(fila[3],{"height":largo,"width":ancho},token) if fila[3] != None else ''
                        val3=self.cloudimg_imagen(fila[4],{"height":largo,"width":ancho},token) if fila[4] != None else ''
                        val4=self.cloudimg_imagen(fila[4],{"height":largo,"width":ancho},token) if fila[5] != None else ''
                        lista=list(fila)                    
                        lista[1]=val
                        lista[2]=val1
                        lista[3]=val2
                        lista[4]=val3
                        lista[5]=val4
                        con_filas=con_filas+1    
                        auxreturn.append(lista)     
                        pass
                    else:
                        val=self.cloudimg_imagen(fila[posicion],{"height":largo,"width":ancho},token) if fila[posicion] != None else ''
                        lista=list(fila)                    
                        lista[posicion]=val
                        con_filas=con_filas+1    
                        auxreturn.append(lista) 
                        print(lista)
                        pass                                            
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
