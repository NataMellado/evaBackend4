from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from pacientes.models import Paciente
from pacientes.api.serializer import PacienteSerializer
from pacientes.api.filters import PacienteFilter

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PacienteFilter
    
    