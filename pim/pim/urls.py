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
from material.views import index,subida,Descarga_doc,Catalogoh,handler404_page,reportenuevo,Descarga_img,carga,Catalogog
from rest_framework.routers import DefaultRouter
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('subida/',subida,name='subida'),
    path('carga/',carga,name='carga'),
    path('Descarga_doc/',Descarga_doc,name='Descarga_doc'), 
    path('catalogog/',Catalogog,name='catalogog'),    
    path('reportenuevo/',reportenuevo,name='reportenuevo'),
    path('Descarga_img/',Descarga_img,name='Descarga_img'),      

]


