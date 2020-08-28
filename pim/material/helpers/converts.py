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
    def convert_array_string(self,array1dimension):
        stringaux=''
        count=1         
        
        for valor in array1dimension:
            if count == len(array1dimension):
                stringaux=stringaux+valor
                    
                pass
            else:
                stringaux=stringaux+valor+","
                count=count+1
                    
            pass
        pass
        
        return  stringaux
        pass


