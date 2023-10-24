from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from .models import Usuario
from .forms import UsuarioForm

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
