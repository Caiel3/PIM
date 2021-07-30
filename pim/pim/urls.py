"""pim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# import sys
# sys.path.append("..")
from material.views import subida,Descarga_doc,Descarga_img,carga,Catalogog,homeview,loginview,user_logout,Consultar_Estado_Tarea,Descargar_Documento_Peticion,Descargar_Imagenes_Peticion,Borrar_Peticion
from rest_framework.routers import DefaultRouter
from django.conf.urls import handler404
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homeview.home,name='index'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('Descargar_Documento/<str:id>', Descargar_Documento_Peticion, name='Descargar_Documento'),
    path('Descargar_Imagenes/<str:id>', Descargar_Imagenes_Peticion, name='Descargar_Imagenes'),
    path('Borrar_Petición/<str:id>', Borrar_Peticion, name='Borrar_Peticion'),
    path('home/',loginview.login,name='home'),
    path('logout/',user_logout,name='logout'),
    path('subida/',subida,name='subida'),
    path('carga/',carga,name='carga'),
    path('Descarga_doc/',Descarga_doc,name='Descarga_doc'), 
    path('catalogog/',Catalogog,name='catalogog'),    
    path('portal/',Consultar_Estado_Tarea,name='portal'),
    path('Descarga_img/',Descarga_img,name='Descarga_img'),      

]


