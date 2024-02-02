from django import forms
from .models import DevolucionProducto, Usuario,Producto,Movimiento

class UsuarioForm(forms.ModelForm):
    # Definir las opciones para el campo 'carrera'
    OPCIONES_CARRERA = [
        ('IngAmbiental', 'Ingeniería Ambiental'),
        ('IngIndustrial', 'Ingeniería Industrial'),
        ('CompIA', 'Ciencias de la Computación e IA'),
        ('IngElectronica', 'Ingeniería Electrónica'),
        ('Matematicas', 'Matemáticas'),
    ]

    # Definir el campo 'carrera' utilizando el widget Select y las opciones
    carrera = forms.ChoiceField(choices=OPCIONES_CARRERA, label='Carrera')

    # Validación personalizada para el campo 'correo_electronico'
    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data.get('correo_electronico')
        if Usuario.objects.filter(correo_electronico=correo_electronico).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return correo_electronico

    # Validación personalizada para el campo 'carnet'
    def clean_carnet(self):
        carnet = self.cleaned_data.get('carnet')
        if Usuario.objects.filter(carnet=carnet).exists():
            raise forms.ValidationError('Este número de carnet ya está registrado.')
        return carnet
    
    def __str__(self):
        return f"{self.nombre} - {self.carrera}"

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo_electronico', 'carrera', 'carnet']
        labels = {
            'nombre': 'Nombre completo',
            'correo_electronico': 'Correo electrónico',
            'carrera': 'Carrera',
            'carnet': 'Número de carnet',
        }
        widgets = {
            'carnet': forms.TextInput(attrs={'placeholder': 'Introduce el UID de carnet'}),
            'correo_electronico': forms.TextInput(attrs={'placeholder': 'Introduce el correo electronico institucional'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Introduce el Nombre completo del estudiante'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'modelo', 'codigo', 'ubicacion', 'otra_ubicacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otra_ubicacion'].required = False
        
class EntregaProductoForm(forms.ModelForm):
    usuario_id = forms.CharField(label='Número de Carnet', max_length=100, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model = Movimiento
        fields = ['usuario_id', 'producto', 'comentario']
        widgets = {
            'usuario_id': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(EntregaProductoForm, self).__init__(*args, **kwargs)
        # Filtrar los productos disponibles
        productos_disponibles = Producto.objects.filter(disponible=True)
        self.fields['producto'].queryset = productos_disponibles

class DevolucionProductoForm(forms.ModelForm):
    class Meta:
        model = DevolucionProducto
        fields = ['producto']

    def __init__(self, *args, **kwargs):
        super(DevolucionProductoForm, self).__init__(*args, **kwargs)
        # Filtrar los productos que actualmente no están disponibles
        productos_no_disponibles = Producto.objects.filter(disponible=False)
        self.fields['producto'].queryset = productos_no_disponibles
