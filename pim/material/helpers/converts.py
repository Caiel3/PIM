from django.db import models
class Converts(models.Model):
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 
    def convert_dic(self,dic):
        mat=[]       
        for reg in dic:
            mat.append(reg)            
            pass
        pass
        return mat 
    def convert_array_string(self,array1dimension,tipo, noesdiccionario=True):        
        stringaux=''
        count=1      
        
        for valor in array1dimension:
            if noesdiccionario:
                if count == len(array1dimension):
                    stringaux=stringaux+valor
                    
                    pass
                else:
                    stringaux=stringaux+valor+","
                    count=count+1
            else:
                if count == len(array1dimension):
                    stringaux=stringaux+valor.get(tipo)
                    
                    pass
                else:
                    stringaux=stringaux+valor.get(tipo)+","
                    count=count+1
                    pass
                pass
        pass
        
        return  stringaux
        pass
    
    def convert_dic_array(diccionario,tipo):        
        vector_consulta=[]    
        for nodo in diccionario:
            vector_consulta.append(nodo[tipo])
            pass
        return vector_consulta
        pass

    def numero_paginas_marca(self,cantidad_prendas):            
        if (cantidad_prendas/4)>round(cantidad_prendas/4):
            return round(cantidad_prendas/4)+1
            pass
        else:
            return(cantidad_prendas/4)
            pass

