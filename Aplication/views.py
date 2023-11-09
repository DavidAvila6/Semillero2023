from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render

from Semillero import settings
from .models import Historial, Movimiento, Producto, Usuario
from .forms import DevolucionProductoForm, UsuarioForm,ProductoForm,EntregaProductoForm,Movimiento
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
    mensaje=None
    if request.method == 'POST':
        form = EntregaProductoForm(request.POST)
        if form.is_valid():
            # Obtener el ID del usuario proporcionado en el formulario
            usuario_id = form.cleaned_data['usuario_id']
            
            usuario = None
            # Intentar obtener el usuario por ID
            try:
                usuario = Usuario.objects.get(carnet=usuario_id)  # Usar .get() en lugar de .filter()
                
            except Usuario.DoesNotExist:
                # Manejar el caso en que el usuario no existe
                # Puedes mostrar un mensaje de error o redirigir a una página de error.
                # Por ejemplo, return render(request, 'error.html')
                pass
            if usuario :
                comentario= form.cleaned_data['comentario']
                
                
                producto_id = form.cleaned_data['producto_id']
                producto = Producto.objects.get(codigo=producto_id)
                valid = Movimiento.objects.filter(producto=producto)

                if valid.exists():
                    mensaje = f'El Producto ya esta con un usuario.'
                else:
                    mensaje = f''
                    movimiento = Movimiento(usuario=usuario, producto=producto,comentario=comentario)
                    movimiento.save()

                # Crear un nuevo objeto de Historial con la misma información
                    historial = Historial(
                    usuario=usuario,
                    producto=movimiento.producto,  # Ajusta esto según tu modelo de Movimiento
                    tipo='Entrega',
                    fecha_movimiento=movimiento.hora_entrega,  # Ajusta esto según tu modelo de Movimiento
                    comentario=movimiento.comentario)
                # Guardar el objeto de Historial en la base de datos
                    historial.save()

                    context = {'movimiento': movimiento}  # Puedes pasar datos adicionales a la plantilla si es necesario
                    html_content = render_to_string('correos/usuario_producto.html', context)


                # Envía un correo electrónico de confirmación con contenido HTML
                    subject = 'Entrega de Producto de SERGIOPLUS'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [usuario.correo_electronico]

                    send_mail(subject, '', from_email, recipient_list, fail_silently=True, html_message=html_content)

                    return redirect('lista_movimientos')  # Redirigir a la lista de movimientos
        

    else:
        form = EntregaProductoForm()

    return render(request, 'entregar_producto.html', {'form': form,'mensaje':mensaje})






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

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')