from django.contrib import admin
from .models import Usuario,Producto,Movimiento,DevolucionProducto,Historial

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Movimiento)
admin.site.register(DevolucionProducto)
admin.site.register(Historial)