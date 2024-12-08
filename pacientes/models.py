from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    edad = models.IntegerField()
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=10)
    email = models.EmailField()
    cant_visitas = models.IntegerField()