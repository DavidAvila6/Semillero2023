from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    carrera = models.CharField(max_length=100)
    carnet = models.CharField(max_length=20, default='valor_predeterminado')  
    def __str__(self):
        return self.nombre

