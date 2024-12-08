from rest_framework.routers import DefaultRouter
from pacientes.api.views import PacienteViewSet

router = DefaultRouter()
router.register('pacientes', PacienteViewSet, basename='paciente')

# path : localhost:3000/api/pacientes

urlpatterns = router.urls