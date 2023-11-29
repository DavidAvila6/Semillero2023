from django.contrib import admin
from .models import Usuario,Producto,Movimiento,DevolucionProducto,Historial,Inventario

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Movimiento)
admin.site.register(DevolucionProducto)
admin.site.register(Historial)
admin.site.register(Inventario)