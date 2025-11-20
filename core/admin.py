from django.contrib import admin
from .models import DetallePedidos, Direcciones, Pedidos, Productos

# Register your models here.

@admin.register(DetallePedidos)
class DetallePedidosAdmin(admin.ModelAdmin):
    pass

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    pass
