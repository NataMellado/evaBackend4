from django.db import models

# Create your models here.
class User(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    edad = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(max_length=50, default='1000-01-01')
    telefono = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    cant_visitas = models.CharField(max_length=50)