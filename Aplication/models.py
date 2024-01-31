from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    carrera = models.CharField(max_length=100, choices=[
        ('IngAmbiental', 'Ingeniería Ambiental'),
        ('IngIndustrial', 'Ingeniería Industrial'),
        ('CompIA', 'Ciencias de la Computación e IA'),
        ('IngElectronica', 'Ingeniería Electrónica'),
        ('Matematicas', 'Matemáticas'),
    ])

    carnet = models.CharField(max_length=20, unique=True)
    correo_electronico = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        # Validación personalizada para garantizar que el correo y el carnet no se repitan
        if Usuario.objects.filter(carnet=self.carnet).exclude(id=self.id).exists():
            raise ValidationError({'carnet': 'Este número de carnet ya está registrado.'})
        
        if Usuario.objects.filter(correo_electronico=self.correo_electronico).exclude(id=self.id).exists():
            raise ValidationError({'correo_electronico': 'Este correo electrónico ya está registrado.'})
    
# en models.py de tu aplicación
class Producto(models.Model):

    OPCIONES_UBICACION = [
        ('A2', 'A2'),
        ('A3', 'A3'),
        ('A4', 'A4'),
        ('A5', 'A5'),
        ('A6', 'A6'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('B3', 'B3'),
        ('B4', 'B4'),
        ('B5', 'B5'),
        ('B6', 'B6'),
        ('C3', 'C3'),
        ('C4', 'C4'),
        ('C5', 'C5'),
        ('C6', 'C6'),
        ('C7', 'C7'),
        ('C8', 'C8'),
        ('T1', 'T1'),
        ('T2', 'T2'),
        ('OTRO', 'Otro'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255, choices=OPCIONES_UBICACION, default='')
    otra_ubicacion = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.nombre} - {self.marca} - {self.codigo} - {self.ubicacion} - {self.modelo}"

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

    def __str__(self):
        return f"{self.Objeto} - {self.ActivoFijo} - {self.Marca}"
