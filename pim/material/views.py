from django.shortcuts import render,redirect
from .models import Materiales,Descarga
from django.http import HttpResponse
import numpy as np
import os
from .helpers.CloudImage import CloudImage
from .helpers.converts import Converts
from .helpers.descarga_imagenes import Descarga_imagenes
from django.db import connection
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,mm
import csv
import io
from django.contrib import messages
from rest_framework import viewsets
from .serializar import MaterialSerializar


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class=MaterialSerializar
    queryset = Materiales.objects.raw('select * from material_materiales limit 10')

def index(request):    
    return render(request,'index.html')

def subida(request):
    consulta=[
        'MATERIAL',
        'DESCRIPCION_MATERIAL',
        'DESCRIPCION_MATERIAL_ENRIQUECIDO',
        'DESCRIPCION_LARGA',
        'EAN',
        'DESCRIPCION_TALLA',
        'DESCRIPCION_COLOR',
        'IMAGEN_GRANDE',
        'TIPO_PRENDA',
        'SUBGRUPO',
        'GENERO',
        'DEPARTAMENTO',
        'CARACTERISTICA',
        'TAGS',
        'GRUPO_DESTINO'
        ]
    parametros=[]
    #Capturamos la informacion del formulario    
    archivo = request.FILES["archivo"]     
    tipo = request.POST["tipo"]
    ancho = request.POST["ancho"]
    largo = request.POST["largo"]   
    for item in consulta:
        if item.upper() in request.POST :
            aux=request.POST[item]
            parametros.append(aux)                            
        pass             
    mi_archivo=request.FILES["archivo"] 
    file = mi_archivo.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file))
    archivo = [line for line in reader]   
    vali=validacion(archivo,tipo)
    if vali:
        messages.error(request,vali)
        print(parametros)
        return render(request,'index.html',{'ancho':ancho,'largo':largo,'tipo':tipo,'consulta':parametros})          
    #Relizamos la consulta nativa en la base de datos
    converts_helper=Converts()  
    string_campos=converts_helper.convert_array_string(parametros,tipo) #no spermite traer un string de campos a partir de un arreglo
    string_filtro=converts_helper.convert_array_string(archivo,tipo,False)
    vector_consulta_descarga=Converts.convert_dic_array(archivo,tipo)    
    #controlo por donde hace la consulta si por ean o material   
    if tipo =="MATERIAL":        
        consulta='select distinct {} from material_materiales where material in ({});'.format(string_campos,string_filtro)       
        consulta_descarga=Materiales.objects.values('ean','imagen_grande').filter(material__in=vector_consulta_descarga)        
                   
    else:
        consulta='select distinct {} from material_materiales where ean in ({});'.format(string_campos,string_filtro)       
        consulta_descarga=Materiales.objects.values('ean','imagen_grande').filter(ean__in=vector_consulta_descarga)       
    #Guardarmos lo que se va a descargar en la base de datos por si se descarga
   
    Descarga.objects.all().delete()
    for valor in consulta_descarga:
        Descarga.objects.create(ean=valor['ean'],imagen_grande="https://{}.cloudimg.io/v7/{}?sharp=1&width={}&height={}".format('aatdtkgdoo',valor['imagen_grande'],ancho,largo))        
    matconsulta=consultasql(consulta)    
    #converitmos todo haciendo uso de cloud img  
    cloud=CloudImage()
    informacion=cloud.convertir_matriz(matconsulta,parametros,ancho,largo,'aatdtkgdoo')      
    return render(request,'visualizacion.html',{"headers":parametros,"lista":informacion,"descarga":consulta_descarga})    
    pass

def Catalogoh(request):
    mi_archivo=request.FILES["archivo"] 
    files = mi_archivo.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(files))
    archivo = [line for line in reader]
    import pdb ; pdb.set_trace()
    for item in reader:
        print(item)
    
 




def consultasql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        mat=cursor.fetchall()
    pass
    return mat

def descarga(request):
    import pdb; pdb.set_trace()
    descarga=Descarga_imagenes()
    descarga.descargar(Descarga.objects.values('ean','imagen_grande').all())
    return render(request,'index.html')
    

def validacion(lista,tipo):        
    if lista:
        if len(lista[0].keys())>1:
            return('Recuerde que solo puede ingresar una lista de eans o materiales, la que tiene actualmente tiene mas de 1 columna')
        else:
            keys=[]
            for li in lista[0]:
                keys.append(li)
                pass 
            con=Converts()
            llave=con.convert_array_string(keys,"")                   
            if(tipo not in  llave.upper()):
                return('Usted seleciono un header {} y ingreso un archivo con header {}, por favor valide.').format(tipo,llave)
            else:
                return (False)
    else:
        return('El documento esta vacio por favor valide')
    pass

def report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=catalogo.pdf'
    archivo=['100243','1003','100304','100308','100309','100326','100344','10036','100361','100378','100396']
    datos=Materiales.objects.filter(material__in=archivo).values()
    import pdb; pdb.set_trace()
    """  datos = [{'Codigo':'7701520374178','Categoria':'Mujer Adulta','Material':'100887','UnidadEmpaque':'1','Tallas':'12-16-18-32','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Mujer_Silueta_Amplia/CAMISETAS_T_SHIRT/Milia1/190x240/Camiseta-Mujer-Silueta-Amplia-Milia1-Blanco-900-Frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
             {'Codigo':'7701520420660','Categoria':'HOMBRES','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'rojo','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/190x240/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'}]
         """
    datos=[{'Codigo':'7701520420660','Categoria':'ADULTOS','Material':'101725','UnidadEmpaque':'1','Tallas':'S-M','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Brandall/566x715/Camiseta-hombre-Brandall-negro-intenso-799-frente-GEF.jpg'},
            {'Codigo':'7701520423470','Categoria':'ADULTOS','Material':'101840','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Mujeres/DEPORTIVO/Rowdy/566x715/Pantalon-mujer-Rowdy-negro-intenso-799-frente-GEF.jpg'},
            {'Codigo':'7701520483702','Categoria':'ADULTOS','Material':'102213','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Mujeres/CAMISETAS_T_SHIRT/Karlita/566x715/Pijama-mujer-Karlita-negro-intenso-799-frente-GEF.jpg'},
            {'Codigo':'7701520531601','Categoria':'ADULTOS','Material':'101221','UnidadEmpaque':'1','Tallas':'S-ML-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Vivant/566x715/Pantalon-hombre-Vivant-negro-intenso-799-frente-GEF.jpg'},
            {'Codigo':'7701520610795','Categoria':'NIÑOS','Material':'104038','UnidadEmpaque':'1','Tallas':'14-16','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Junior_Masculino/ROPA_INTERIOR/Clinton_Junior/566x715/Pantaloncillo-juvenil-masculino-Clinton-Junior-negro-intenso-799-frente-GEF.jpg'},
            {'Codigo':'7701520644080','Categoria':'ADULTOS','Material':'103616','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Gris','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/ROPA_INTERIOR/Duo_Clinton_2/566x715/Boxer-Hombre-Duo-Clinton-2-Gris-Humo-707-Frente2-GEF.jpg'},
            {'Codigo':'7701520661537','Categoria':'ADULTOS','Material':'104334','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Blanco','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Mujeres/PIJAMAS/Amylita_T_shirt/566x715/Pijama-Mujer-joven-Amylita-T-Shirt-Blanco-900-Frente-Gef.jpg'},
            {'Codigo':'7701520663548','Categoria':'ADULTOS','Material':'101221','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Azul','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Vivant/566x715/Pantalon-hombre-Vivant-azul-5650-frente-GEF.jpg'},
            {'Codigo':'7701520666280','Categoria':'ADULTOS','Material':'104413','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Blanco','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Mujeres/CAMISETAS_T_SHIRT/Angara/566x715/Camiseta-mujer-Angara-blanco-905-frente-GEF.jpg'},
            {'Codigo':'7701520667515','Categoria':'ADULTOS','Material':'104601','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/ROPA_INTERIOR/Ennael/566x715/Camiseta-hombre-Ennael-negro-intenso-799-frente-GEF.jpg'},
            {'Codigo':'7701520672175','Categoria':'ADULTOS','Material':'104819','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro-Blanco','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/ROPA_INTERIOR/Muzzarelli/566x715/Pantaloncillo-hombre-muzzarelli-negro-intenso-799-frente-GEF.jpg'},
            {'Codigo':'7701520672410','Categoria':'ADULTOS','Material':'104828','UnidadEmpaque':'1','Tallas':'S-M-L-XL','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro-Blanco','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Mussons/566x715/Camiseta-Hombre-Mussons-Negro-799-Frente-Gef.jpg'},
            {'Codigo':'7701520677002','Categoria':'ADULTOS','Material':'104947','UnidadEmpaque':'1','Tallas':'32-34-36-38-40-42','Composicion':'78% ALGODON 20% poliester 2% elasta','color':'Negro-Blanco','Imagen':'http://www.gef.com.co/wcsstore/CrystalCo_CAT_AS/Gef/ES-CO/Imagenes/Masculino_Exterior/PIJAMAS/Cadiz/566x715/Camiseta-hombre-Cadiz-Alg-blanco-900-frente-GEF.jpg'}
            ]
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    y = 740
    registroxhoja= 0
    c.setLineWidth(.3)
    c.setFont('Helvetica-Bold',11)
    for val in datos:
        if registroxhoja == 4:
            registroxhoja = 0
            y = 740
            c.showPage()
        
        c.drawImage(val['Imagen'], 35, y-130, 140, 160)
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Categoria:')
        c.setFont('Helvetica',11)
        c.drawString(245,y,val['Categoria'])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Colección:')
        c.setFont('Helvetica',11)
        c.drawString(245,y,'Año 2020 Vestuario/Básico/Línea 2do Sem/Salir')
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Material:')
        c.setFont('Helvetica',11)
        c.drawString(230,y,val['Material'])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Composición:')
        c.setFont('Helvetica',11)
        c.drawString(265,y,val['Composicion'])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Unidad de empaque:')
        c.setFont('Helvetica',11)
        c.drawString(300,y,val['UnidadEmpaque'])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Color:')
        c.setFont('Helvetica',11)
        c.drawString(220,y,val['color'])
        y = y - 16
        c.setFont('Helvetica-Bold',12)
        c.drawString(180,y,'Tallas:')
        c.setFont('Helvetica',11)
        c.drawString(220,y,val['Tallas'])
        y = y - 40
        c.line(35,y,560,y)
        y = y - 40
        registroxhoja = registroxhoja+1

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

