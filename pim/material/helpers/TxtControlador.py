from django.conf import settings
import os.path as path

class Txt():
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 
    
    def __init__(self,hash,texto,fecha_ini,fecha_fin):        
        self.hash=hash
        self.fecha_ini=fecha_ini.strftime('%d/%m/%Y %H:%M.%S')
        self.fecha_fin=fecha_fin.strftime('%d/%m/%Y %H:%M.%S')
        self.Escribir_log(texto)
    
    def Escribir_log(self,log_texto):
        try:           
            text= 'inicio {}: {} Fin: {}'.format(self.fecha_ini,log_texto,self.fecha_fin)
            dire=settings.MEDIA_ROOT+"/log/"+self.hash+'.txt'
            if path.exists(dire):
                with open(dire,'a', encoding='UTF-8') as log:
                    log.write(text+' \n ')
                    log.close()
            else:
                log=open(dire,'w',encoding='UTF-8')
                log.write(log_texto)
                log.close()
        except Exception as ex:
          print('Something went wrong'+ex)
        


