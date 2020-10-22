from django.contrib import admin
from .models import Materiales,MysqlColores,MysqlMateriales,MysqlTallas,Tipo_Prenda,Grupo_Destino,Genero,Marca,Orden_Tallas
# Register your models here.

admin.site.register(Materiales)
admin.site.register(MysqlColores)
admin.site.register(MysqlMateriales)
admin.site.register(MysqlTallas)
admin.site.register(Tipo_Prenda)
admin.site.register(Grupo_Destino)
admin.site.register(Genero)
admin.site.register(Marca)
admin.site.register(Orden_Tallas)