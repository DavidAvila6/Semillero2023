from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from .models import Movimiento, Producto, Usuario
from .forms import UsuarioForm,ProductoForm,EntregaProductoForm,Movimiento

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
            form.save()  # Guardar la entrega del producto en la base de datos
            return redirect('lista_movimientos')  # Redirigir a la lista de movimientos
    else:
        form = EntregaProductoForm()
    
    return render(request, 'entregar_producto.html', {'form': form})

def lista_movimientos(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'lista_movimientos.html', {'movimientos': movimientos})

def informacion_movimiento(request, movimiento_id):
    movimiento = Movimiento.objects.select_related('usuario', 'producto').get(pk=movimiento_id)
    context = {'movimiento': movimiento}
    return render(request, 'informacion_movimiento.html', context)
