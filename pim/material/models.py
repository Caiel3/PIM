from django.db import models

# Create your models here.

class Materiales(models.Model):
    material = models.TextField(db_column='MATERIAL', blank=True, null=True)  
    descripcion_material = models.TextField(db_column='DESCRIPCION_MATERIAL', blank=True, null=True)  
    descripcion_material_enriquecido = models.TextField(db_column='DESCRIPCION_MATERIAL_ENRIQUECIDO', blank=True, null=True)  
    descripcion_larga = models.TextField(db_column='DESCRIPCION_LARGA', blank=True, null=True)  
    ean = models.CharField(db_column='EAN', blank=True, max_length=30, primary_key=True)  
    codigo_talla = models.TextField(db_column='CODIGO_TALLA', blank=True, null=True)  
    descripcion_talla = models.TextField(db_column='DESCRIPCION_TALLA', blank=True, null=True)  
    codigo_color = models.TextField(db_column='CODIGO_COLOR', blank=True, null=True)  
    descripcion_color = models.TextField(db_column='DESCRIPCION_COLOR', blank=True, null=True)  
    imagen_pequena = models.TextField(db_column='IMAGEN_PEQUENA', blank=True, null=True)  
    imagen_grande = models.TextField(db_column='IMAGEN_GRANDE', blank=True, null=True)  
    imagen_frente = models.TextField(db_column='IMAGEN_FRENTE', blank=True, null=True)  
    imagen_espalda = models.TextField(db_column='IMAGEN_ESPALDA', blank=True, null=True)  
    imagen_detalle = models.TextField(db_column='IMAGEN_DETALLE', blank=True, null=True)  
    imagen_detalle2 = models.TextField(db_column='IMAGEN_DETALLE2', blank=True, null=True)  
    tipo_prenda = models.TextField(db_column='TIPO_PRENDA', blank=True, null=True)  
    subgrupo = models.TextField(db_column='SUBGRUPO', blank=True, null=True)  
    caracteristica = models.TextField(db_column='CARACTERISTICA', blank=True, null=True)  
    marca = models.TextField(db_column='MARCA', blank=True, null=True)  
    uso = models.TextField(db_column='USO', blank=True, null=True)  
    grupo_destino = models.TextField(db_column='GRUPO_DESTINO', blank=True, null=True)  
    genero = models.TextField(db_column='GENERO', blank=True, null=True)  
    departamento = models.TextField(db_column='DEPARTAMENTO', blank=True, null=True)  
    tags = models.TextField(db_column='TAGS', blank=True, null=True)  
    prendido_ecommerce = models.IntegerField(db_column='PRENDIDO_ECOMMERCE', blank=True, null=True)  
    prendido_ean = models.IntegerField(db_column='PRENDIDO_EAN', blank=True, null=True)  
    fecha_actualizacion = models.DateTimeField(db_column='FECHA_ACTUALIZACION', blank=True, null=True)  

    def __str__(self):
        return "Material: {}, Descripcion: {}, Ean: {}".format(self.material,self.descripcion_material,self.ean)
        