from django.conf import settings
import os
class Limpiar():
    
    def __str__(self):
        return 

    def __unicode__(self):
        return 
    
    def limpiar_media_imagenes():
        dire=settings.MEDIA_ROOT+"/Imagenes_descarga"
        carpeta=os.walk(dire)    
        
        for folder, subfolders, files in carpeta:
            for file in files:
                if files:
                    os.remove(folder+'/'+file)
                pass
         