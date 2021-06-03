# PIM
implementacion con django

VIRTUAL ENV_________________________
virtualenv libs

LIBRERIAS___________________________
pip install D:\Temp\PIM\mysqlclient-1.4.6-cp38-cp38-win32.whl
pip install django
pip install numpy
pip install reportlab
pip install requests
pip install djangorestframework
pip install django-cors-header
pip install pymysql


PROYECTO Y APLICACIONES_____________
django-admin startproject pim --Crear proyecto
django-admin startapp material --Crear apps en carpeta
python manage.py startapp


CAMBIOS BASE DE DATOS_______________
python manage.py makemigrations --Crear una migracion para preparar la estructura de la base de datos
python manage.py migration --Migrar todo a la base de datos
Python manage.py inspectdb > material/models.py--traer estructura base de datos

Python manage.py runserver --Ejecutar servidor
python manage.py createsuperuser



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




Debug--
import pdb; pdb.set_trace()

Celery_______
celery -A pim  worker -l info