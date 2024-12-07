from rest_framework import viewsets
from pacientes.models import Paciente
from pacientes.api.serializer import PacienteSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer