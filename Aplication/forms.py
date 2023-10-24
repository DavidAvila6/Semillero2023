from django import forms
from .models import Usuario,Producto,Movimiento

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre','correo_electronico', 'carrera', 'carnet']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class EntregaProductoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['usuario', 'producto']
