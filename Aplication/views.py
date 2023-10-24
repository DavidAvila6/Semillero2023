from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from .models import Historial, Movimiento, Producto, Usuario
from .forms import DevolucionProductoForm, UsuarioForm,ProductoForm,EntregaProductoForm,Movimiento

def usuarios(request):
    return render(request, 'usuarios.html')

def productos(request):
    return render(request, 'productos.html')

def movimientos(request):
    return render(request, 'movimientos.html')

def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Puedes hacer ajustes en el campo id aquí si es necesario
            usuario.save()
            return redirect('listar_usuarios')  # Ajusta según el nombre de tu vista de lista de usuarios
    else:
        form = UsuarioForm()

    return render(request, 'formulario_usuario.html', {'form': form})

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def principal(request):
    return render(request, 'principal.html')

def informacion_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    return render(request, 'informacion_usuario.html', {'usuario': usuario})

def verificar_carnet(request):
    mensaje = None

    if request.method == 'POST':
        carnet = request.POST['carnet']
        usuarios = Usuario.objects.filter(carnet=carnet)

        if usuarios.exists():
            mensaje = f'El carnet {carnet} ya existe en la base de datos.'
        else:
            mensaje = f'El carnet {carnet} no existe en la base de datos.'

    return render(request, 'verificar_carnet.html', {'mensaje': mensaje})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

def listar_productos(request):
    productos = Producto.objects.all()  # Recupera todos los productos de la base de datos
    return render(request, 'lista_productos.html', {'productos': productos})

def informacion_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'informacion_producto.html', {'producto': producto})

def entregar_producto(request):
    if request.method == 'POST':
        form = EntregaProductoForm(request.POST)
        if form.is_valid():
            # Guardar la entrega del producto en la tabla de Movimiento
            movimiento = form.save()
            
            # Crear un nuevo objeto de Historial con la misma información
            historial = Historial(
                usuario=movimiento.usuario, 
                producto=movimiento.producto, 
                tipo='Entrega',
                fecha_movimiento=movimiento.hora_entrega)
            
            # Guardar el objeto de Historial en la base de datos
            historial.save()

            return redirect('lista_movimientos')  # Redirigir a la lista de movimientos
    else:
        form = EntregaProductoForm()
    
    return render(request, 'entregar_producto.html', {'form': form})

def devolver_producto(request):
    if request.method == 'POST':
        form = DevolucionProductoForm(request.POST)
        if form.is_valid():
            codigo_producto = form.cleaned_data['codigo_producto']
            
            # Verifica si el código del producto está en la lista de movimientos
            try:
                movimiento = Movimiento.objects.get(producto__codigo=codigo_producto)
                movimiento.delete()  # Elimina el registro de movimiento
                # Crear un nuevo objeto de Historial con la misma información
                historial = Historial(
                    usuario=movimiento.usuario, 
                    producto=movimiento.producto, 
                    tipo='Devolucion',
                    fecha_movimiento=movimiento.hora_entrega)
                
                # Guardar el objeto de Historial en la base de datos
                historial.save()
                return redirect('lista_movimientos')
            except Movimiento.DoesNotExist:
                # El código del producto no se encontró en los movimientos
                return render(request, 'devolver_producto.html', {'form': form, 'error': 'Producto no encontrado en la lista de movimientos'})
    else:
        form = DevolucionProductoForm()
    
    return render(request, 'devolver_producto.html', {'form': form})

def lista_movimientos(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'lista_movimientos.html', {'movimientos': movimientos})

def informacion_movimiento(request, movimiento_id):
    movimiento = Movimiento.objects.select_related('usuario', 'producto').get(pk=movimiento_id)
    context = {'movimiento': movimiento}
    return render(request, 'informacion_movimiento.html', context)

def historial(request):
    historial = Historial.objects.all()

    return render(request, 'historial_movimientos.html', {'historial': historial})

def informacion_historial(request, historial_id):
    historial = get_object_or_404(Historial, pk=historial_id)  # Asegúrate de importar el modelo Historial
    return render(request, 'informacion_historial.html', {'historial': historial})
