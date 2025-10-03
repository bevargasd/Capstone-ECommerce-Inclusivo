from django.contrib import admin
from .models import DetallePedidos, Direcciones, Pedidos, Productos, Usuarios

# Register your models here.

@admin.register(DetallePedidos)
class DetallePedidosAdmin(admin.ModelAdmin):
    pass

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    pass
