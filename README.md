# PIM
implementacion con django

VIRTUAL ENV_________________________
virtualenv libs

LIBRERIAS___________________________
pip install D:\Temp\PIM\mysqlclient-1.4.6-cp38-cp38-win32.whl
pip install django



PROYECTO Y APLICACIONES_____________
django-admin startproject pim --Crear proyecto
django-admin startapp material --Crear apps en carpeta
python manage.py startapp


CAMBIOS BASE DE DATOS_______________
python manage.py makemigrations --Crear una migracion para preparar la estructura de la base de datos
python manage.py migration --Migrar todo a la base de datos
Python manage.py inspectdb > material/models.py--traer estructura base de datos

Python manage.py runserver --Ejecutar servidor




CONFIGURACION BASE DE DATOS_____________
DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
		'USER' : 'root',
        'PASSWORD':'r0o7_Sq1_cri5T@l_8193',
		'NAME' : 'RAM',
		'HOST':'172.18.175.114',
		'PORT' : '3306',
		'OPTIONS': {
			'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
			# Tell MySQLdb to connect with 'utf8mb4' character set
            'charset': 'utf8mb4',
		},
		# Tell Django to build the test database with the 'utf8mb4' character set
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        }
    }
}





class Materiales(models.Model):
    material = models.TextField(db_column='MATERIAL', blank=True, null=True)  
    descripcion_material = models.TextField(db_column='DESCRIPCION_MATERIAL', blank=True, null=True)  
    descripcion_material_enriquecido = models.TextField(db_column='DESCRIPCION_MATERIAL_ENRIQUECIDO', blank=True, null=True)  
    descripcion_larga = models.TextField(db_column='DESCRIPCION_LARGA', blank=True, null=True)  
    ean = models.TextField(db_column='EAN', blank=True, null=True)  
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
