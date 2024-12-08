from django_filters import rest_framework as filters
from pacientes.models import Paciente

class PacienteFilter(filters.FilterSet):
    menor_de_edad = filters.BooleanFilter(method='filter_menor_de_edad', label='Menor de edad')
    mayor_de_edad = filters.BooleanFilter(method='filter_mayor_de_edad', label='Mayor de edad')
    muchas_visitas = filters.BooleanFilter(method='filter_muchas_visitas', label='Muchas visitas')
    
    class Meta:
        model = Paciente
        fields = {
        'nombre': ['icontains'],  # Buscar por nombre (case-insensitive)
        'apellidos': ['icontains'],  # Buscar por apellidos
        'edad': ['lt', 'gt', 'exact'],  # Filtrar por edad menor, mayor o igual
    }
        
    def filter_menor_de_edad(self, queryset, name, value):
        if value:
            return queryset.filter(edad__lt=18)
        return queryset
    
    def filter_mayor_de_edad(self, queryset, name, value):
        if value:
            return queryset.filter(edad__gte=18)
        return queryset
    
    def filter_muchas_visitas(self, queryset, name, value):
        if value:
            return queryset.filter(cant_visitas__gt=400)
        return queryset
        