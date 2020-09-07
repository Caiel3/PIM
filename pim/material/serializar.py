from rest_framework import serializers
from .models import Materiales

class MaterialSerializar(serializers.ModelSerializer):
    class Meta:
        model=Materiales
        fields='__all__'
    
   