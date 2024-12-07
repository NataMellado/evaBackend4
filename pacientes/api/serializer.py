from rest_framework import serializers
from pacientes.models import Paciente

class ProductoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Paciente
        fields = '__all__'
        
        
        
        
        
        