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
    modelo = models.TextField(db_column='MODELO', blank=True, null=True)   
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
    fecha_actualizacion = models.DateTimeField(db_column='FECHA_ACTUALIZACION', blank=True, null=True)  
    composicion_es = models.TextField(db_column='COMPOSICION_ES', blank=True, null=True)   
    tipo_material = models.TextField(db_column='TIPO_MATERIAL', blank=True, null=True)
    origen = models.TextField(db_column='ORIGEN', blank=True, null=True)
    url_catalogo = models.TextField(db_column='URL_CATALOGO', blank=True, null=True)
    url_imagen = models.TextField(db_column='URL_IMAGEN', blank=True, null=True)

    def __str__(self):
        return "Material: {}, Descripcion: {}, Ean: {}".format(self.material,self.descripcion_material,self.ean)
        
class Descarga(models.Model):
    ean = models.CharField(db_column='EAN', blank=True, max_length=30, primary_key=True)  
    imagen_grande = models.TextField(db_column='IMAGEN_GRANDE', blank=True, null=True)  
   
class Catalogo_temp(models.Model):   
    autoincrementable = models.AutoField(db_column='autoincrementable',default=None,primary_key=True)
    material = models.CharField(db_column='MATERIAL', blank=True, max_length=30)  
    unidad_empaque = models.TextField(db_column='UNIDAD_EMPAQUE', blank=True, null=True)
    precio = models.TextField(db_column='PRECIO', blank=True, null=True)
    moneda = models.TextField(db_column='MONEDA', blank=True, null=True)
    pais = models.TextField(db_column='PAIS', blank=True, null=True)
    coleccion=models.TextField(db_column='COLECCION', blank=True, null=True)
    hash_uuid=models.TextField(db_column='HASH_UUID', blank=True, null=True)
    class Meta:
        unique_together = (("material","hash_uuid"),)


class MysqlColores(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    material = models.CharField(db_column='MATERIAL', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descripcion_color = models.CharField(db_column='DESCRIPCION_COLOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    icono_color = models.CharField(db_column='ICONO_COLOR', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:       
        db_table = 'MYSQL_COLORES'


class MysqlMateriales(models.Model):
    material = models.CharField(db_column='MATERIAL', primary_key=True, max_length=30)  # Field name made lowercase.
    descripcion_material = models.CharField(db_column='DESCRIPCION_MATERIAL', max_length=300, blank=True, null=True)  # Field name made lowercase.
    imagen = models.CharField(db_column='IMAGEN', max_length=800, blank=True, null=True)  # Field name made lowercase.
    tipo_prenda = models.CharField(db_column='TIPO_PRENDA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    departamento = models.CharField(db_column='DEPARTAMENTO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marca = models.CharField(db_column='MARCA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    composicion_es = models.CharField(db_column='COMPOSICION_ES', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:        
        db_table = 'MYSQL_MATERIALES'


class MysqlTallas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    material = models.CharField(db_column='MATERIAL', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descripcion_talla = models.CharField(db_column='DESCRIPCION_TALLA', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:        
        db_table = 'MYSQL_TALLAS'


class Tipo_Prenda(models.Model):
    id=models.CharField(db_column='Codigo',primary_key=True,max_length=50)
    Tipo_Prenda = models.CharField(db_column='Tipo_prenda',null=True,max_length=50)    
    class Meta:
        db_table='Tipo_Prenda'

class Grupo_Destino(models.Model):
    id=models.CharField(db_column='Codigo',primary_key=True,max_length=50)
    Grupo_Destino = models.CharField(db_column='Grupo_destino',null=True,max_length=50)
    Tipo_Prenda=models.ManyToManyField(Tipo_Prenda)
    class Meta:
        db_table='Grupo_Destino'

class Genero(models.Model):
    id=models.CharField(db_column='Codigo',primary_key=True,max_length=50)
    Genero = models.CharField(db_column='Genero',null=True,max_length=30)
    Grupo_Destino=models.ManyToManyField(Grupo_Destino)
    class Meta:
        db_table='Genero'

class Marca(models.Model):
    id=models.CharField(db_column='Codigo',primary_key=True,max_length=50)
    marca = models.CharField(db_column='Marca',null=True,max_length=30)
    Genero=models.ManyToManyField(Genero)

    class Meta:
        db_table='Marca'


class Orden_Tallas(models.Model):
    id=models.CharField(db_column='Descripcion_talla',primary_key=True,max_length=30)
    marca = models.IntegerField(db_column='Orden',null=True)  

    class Meta:
        db_table='Orden_Tallas'


class MysqlImagenes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ean = models.CharField(db_column='EAN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    imagen = models.CharField(db_column='IMAGEN', max_length=500, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:       
        db_table = 'MYSQL_IMAGENES'



