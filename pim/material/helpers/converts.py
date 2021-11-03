from math import  floor
from pathlib import Path
import json
import os

class Converts():
    
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
    def convert_array_string(self,array1dimension,tipo,delimitador, noesdiccionario=True):
        stringaux=''
        count=1      
        
        for valor in array1dimension:
            if valor==None:
                valor=''
                pass
            if noesdiccionario:
                if count == len(array1dimension):
                    stringaux=stringaux+valor
                    
                    pass
                else:
                    stringaux=stringaux+valor+delimitador
                    count=count+1
            else:
                if count == len(array1dimension):
                    stringaux=stringaux+valor.get(tipo)
                    
                    pass
                else:
                    stringaux=stringaux+valor.get(tipo)+delimitador
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
        if (cantidad_prendas/4)>floor(cantidad_prendas/4):
            return ((floor (cantidad_prendas/4)+1)*1511.5)
            pass
        else:
            return (cantidad_prendas/4)*1511.5
            pass

    def convert_string_array(self,tipo):
        lista = []
        arreglo = tipo.splitlines()

        for nodo in arreglo:
            if nodo !='' and nodo.isdigit()== True:
                lista.append(nodo)
        return lista
        pass

    def convert_array_str(self,array1dimension,delimitador, noesdiccionario=True):
        stringaux=''
        count=1      
        
        for valor in array1dimension:
            if valor==None:
                valor=''
                pass
            if noesdiccionario:
                if count == len(array1dimension):
                    stringaux=stringaux+valor
                    
                    pass
                else:
                    stringaux=stringaux+valor+delimitador
                    count=count+1
            else:
                if count == len(array1dimension):
                    stringaux=stringaux+valor
                    
                    pass
                else:
                    stringaux=stringaux+valor+delimitador
                    count=count+1
                    pass
                pass
        pass
        return  stringaux
        pass

    def convert_array_str_consulta(self,array1dimension,delimitador, noesdiccionario=True):
        stringaux=''
        count=1      
        
        for valor in array1dimension:
            if valor==None:
                valor=''
                pass
            if noesdiccionario:
                if count == len(array1dimension):
                    stringaux= stringaux + "'"+ valor + "'"
                    
                    pass
                else:
                    stringaux=stringaux + "'"+ valor + "'" + delimitador
                    count=count+1
            else:
                if count == len(array1dimension):
                    stringaux= stringaux + "'"+ valor + "'"
                    
                    pass
                else:
                    stringaux= stringaux + "'"+ valor + "'" + delimitador
                    count=count+1
                    pass
                pass
        pass
        return  stringaux
        pass

    