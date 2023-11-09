"""
URL configuration for Semillero project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Aplication import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.principal),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('principal/', views.principal, name='principal'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('listar-usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('verificar-carnet/', views.verificar_carnet, name='verificar_carnet'),
    path('usuario/<int:usuario_id>/', views.informacion_usuario, name='informacion_usuario'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('listar-productos/', views.listar_productos, name='listar_productos'),
    path('producto/<int:producto_id>/', views.informacion_producto, name='informacion_producto'),
    path('entregar-producto/', views.entregar_producto, name='entregar_producto'),
    path('lista-movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('movimiento/<int:movimiento_id>/', views.informacion_movimiento, name='informacion_movimiento'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('productos/', views.productos, name='productos'),
    path('movimientos/', views.movimientos, name='movimientos'),
    path('devolver_producto/', views.devolver_producto, name='devolver_producto'),
    path('historial/', views.historial, name='historial'),
    path('historial/<int:historial_id>/', views.informacion_historial, name='informacion_historial'),
    
    
    


]
