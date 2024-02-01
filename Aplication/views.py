from io import BytesIO
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render, redirect
from django.views import View
from django.template.loader import get_template  # Para la exportación PDF
from openpyxl import Workbook
from django.contrib import messages
from django.contrib.auth.views import LoginView
from Semillero import settings
from .models import Historial, Movimiento, Producto, Usuario
from .forms import DevolucionProductoForm, UsuarioForm,ProductoForm,EntregaProductoForm,Movimiento
from django.core.mail import send_mail
from django.template.loader import render_to_string

def usuarios(request):
    return render(request, 'pages/usuarios/usuarios.html')

def productos(request):
    return render(request, 'pages/productos/productos.html')

def movimientos(request):
    return render(request, 'pages/movimientos/movimientos.html')

def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Puedes hacer ajustes en el campo id aquí si es necesario
            usuario.save()

            # Renderiza el contenido HTML desde la plantilla
            context = {'user': usuario}  # Puedes pasar datos adicionales a la plantilla si es necesario
            html_content = render_to_string('correos/emailpage.html', context)


                # Envía un correo electrónico de confirmación con contenido HTML
            subject = 'Bienvenido a Nuestra Aplicación'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [usuario.correo_electronico]

            send_mail(subject, '', from_email, recipient_list, fail_silently=True, html_message=html_content)

            return redirect('listar_usuarios')  # Ajusta según el nombre de tu vista de lista de usuarios
    else:
        form = UsuarioForm()

    return render(request, 'pages/usuarios/formulario_usuario.html', {'form': form})

ICONOS_CARRERA = {
    'IngAmbiental': 'bx bxs-leaf',
    'IngIndustrial': 'bx bxs-cog',
    'CompIA': 'bx bx-desktop',
    'IngElectronica': 'bx bxs-wrench',
    'Matematicas': 'bx bxs-calculator',
}

def listar_usuarios(request):
    usuarios = Usuario.objects.all()

    # Agrega un campo 'icono' a cada usuario en función de su carrera
    for usuario in usuarios:
        usuario.icono = ICONOS_CARRERA.get(usuario.carrera, 'bx bxs-user')

    return render(request, 'pages/usuarios/lista_usuarios.html', {'usuarios': usuarios})

def principal(request):
    return render(request, 'pages/principal/principal.html')

def informacion_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    return render(request, 'pages/usuarios/informacion_usuario.html', {'usuario': usuario})

def verificar_carnet(request):
    mensaje = None

    if request.method == 'POST':
        carnet = request.POST['carnet']
        usuarios = Usuario.objects.filter(carnet=carnet)

        if usuarios.exists():
            mensaje = f'El carnet {carnet} ya existe en la base de datos.'
        else:
            mensaje = f'El carnet {carnet} no existe en la base de datos.'

    return render(request, 'pages/usuarios/verificar_carnet.html', {'mensaje': mensaje})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'pages/productos/agregar_producto.html', {'form': form})

def listar_productos(request):
    productos = Producto.objects.all()  # Recupera todos los productos de la base de datos
    return render(request, 'pages/productos/listar_productos.html', {'productos': productos})

def informacion_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'pages/productos/informacion_producto.html', {'producto': producto})
def entregar_producto(request):
    mensaje = None

    if request.method == 'POST':
        form = EntregaProductoForm(request.POST)
        if form.is_valid():
            # Obtener el ID del usuario proporcionado en el formulario
            usuario_id = form.cleaned_data['usuario_id']
            
            usuario = None
            # Intentar obtener el usuario por ID
            try:
                usuario = Usuario.objects.get(carnet=usuario_id)
            except Usuario.DoesNotExist:
                # Manejar el caso en que el usuario no existe
                mensaje = 'Usuario no encontrado. Por favor, registra al usuario antes de hacer el préstamo.'
                return render(request, 'pages/productos/entregar_producto.html', {'form': form, 'mensaje': mensaje})

            comentario = form.cleaned_data['comentario']
            producto_id = form.cleaned_data['producto_id']
            producto = Producto.objects.get(codigo=producto_id)
            valid = Movimiento.objects.filter(producto=producto)

            if valid.exists():
                mensaje = 'El Producto ya está con un usuario.'
            else:
                mensaje = ''
                movimiento = Movimiento(usuario=usuario, producto=producto, comentario=comentario)
                movimiento.save()

                # Crear un nuevo objeto de Historial con la misma información
                historial = Historial(
                    usuario=usuario,
                    producto=movimiento.producto,
                    tipo='Entrega',
                    fecha_movimiento=movimiento.hora_entrega,
                    comentario=movimiento.comentario)
                # Guardar el objeto de Historial en la base de datos
                historial.save()

                context = {'movimiento': movimiento}
                html_content = render_to_string('correos/usuario_producto.html', context)

                # Envía un correo electrónico de confirmación con contenido HTML
                subject = 'Entrega de Producto de SERGIOPLUS'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [usuario.correo_electronico]

                send_mail(subject, '', from_email, recipient_list, fail_silently=True, html_message=html_content)

                return redirect('lista_movimientos')  # Redirigir a la lista de movimientos

    else:
        form = EntregaProductoForm()

    return render(request, 'pages/productos/entregar_producto.html', {'form': form, 'mensaje': mensaje})

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
                return render(request, 'pages/productos/devolver_producto.html', {'form': form, 'error': 'Producto no encontrado en la lista de movimientos'})
    else:
        form = DevolucionProductoForm()
    
    return render(request, 'pages/productos/devolver_producto.html', {'form': form})

def lista_movimientos(request):
    movimientos = Movimiento.objects.all()
    return render(request, 'pages/movimientos/lista_movimientos.html', {'movimientos': movimientos})

def informacion_movimiento(request, movimiento_id):
    movimiento = Movimiento.objects.select_related('usuario', 'producto').get(pk=movimiento_id)
    context = {'movimiento': movimiento}
    return render(request, 'pages/movimientos/informacion_movimiento.html', context)

def historial(request):
    historial = Historial.objects.all()

    return render(request, 'pages/movimientos/historial_movimientos.html', {'historial': historial})

def informacion_historial(request, historial_id):
    historial = get_object_or_404(Historial, pk=historial_id)  # Asegúrate de importar el modelo Historial
    return render(request, 'pages/movimientos/informacion_historial.html', {'historial': historial})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            auth_login(request, usuario)
            messages.success(request, f'Bienvenido, {usuario.username}!')
            return redirect('principal')  # Corregido el nombre de la vista principal
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def cerrar_sesion(request):
    auth_logout(request)
    messages.info(request, '¡Has cerrado sesión exitosamente!')
    return redirect('login')  

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            auth_login(request, usuario)
            messages.success(request, f'Bienvenido, {usuario.username}! Te has registrado exitosamente.')
            return redirect('pages/principal/principal.html')  # Ajusta según el nombre de tu vista principal
    else:
        form = UserCreationForm()
    return render(request, 'auth/registro.html', {'form': form})