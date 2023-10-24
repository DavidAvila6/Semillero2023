from django.contrib import admin
from .models import Usuario,Producto,Movimiento

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Movimiento)