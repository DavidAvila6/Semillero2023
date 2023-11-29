from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    carrera = models.CharField(max_length=100)
    carnet = models.CharField(max_length=20)
    correo_electronico = models.EmailField(max_length=255)
    def __str__(self):
        return self.nombre
    
# en models.py de tu aplicación
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255, default='Ningún modelo')
    codigo = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255, default='N/A')
    utilidad = models.CharField(max_length=255, default='N/A')

    def __str__(self):
        return f"{self.nombre} - {self.marca} - {self.codigo}"


class Movimiento(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    hora_entrega = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True, default='Ningún Comentario')

    def __str__(self):
        return f'Movimiento de {self.usuario} para {self.producto} a las {self.hora_entrega}'

class DevolucionProducto(models.Model):
    codigo_producto = models.CharField(max_length=50)



class Historial(models.Model):
    
    tipo = models.CharField(max_length=10)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True, default='Ningún Comentario')

    def __str__(self):
        return f"{self.tipo} - {self.producto} - {self.usuario}"


class Inventario(models.Model):
    ActivoFijo = models.CharField(max_length=255)
    Objeto = models.CharField(max_length=255)
    Marca = models.CharField(max_length=255)
    Modelo = models.CharField(max_length=255)
    Ubicacion = models.CharField(max_length=255)
    Utilidad = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.Objeto} - {self.ActivoFijo} - {self.Marca}"
