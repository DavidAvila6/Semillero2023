from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    carrera = models.CharField(max_length=100)
    carnet = models.CharField(max_length=20)
    correo_electronico = models.EmailField(max_length=255)
    def __str__(self):
        return self.nombre

