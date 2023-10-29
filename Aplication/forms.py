from django import forms
from .models import DevolucionProducto, Usuario,Producto,Movimiento

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre','correo_electronico', 'carrera', 'carnet']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class EntregaProductoForm(forms.ModelForm):
    usuario_id = forms.CharField(label='ID del Usuario')
    producto_id = forms.CharField(label='ID del Producto')

    class Meta:
        model = Movimiento
        fields = ['usuario_id', 'producto_id']

class DevolucionProductoForm(forms.ModelForm):
    codigo_producto = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    class Meta:
        model = DevolucionProducto
        fields = ['codigo_producto']
