from django.db import models
from django.contrib.auth.models import User   # usamos Django auth

# ============================================================
# CATEGORÍAS
# ============================================================

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.nombre


# ============================================================
# PRODUCTOS
# ============================================================

class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=120, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )

    imagen_uno = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_dos = models.ImageField(upload_to='productos/', blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return self.nombre

# ============================================================
# DIRECCIONES 
# ============================================================

class Direcciones(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        null=True
    )
    calle = models.CharField(max_length=150)
    numero = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'direcciones'

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.ciudad}"


# ============================================================
# PEDIDOS
# ============================================================

class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    id_direccion = models.ForeignKey(
        Direcciones,
        on_delete=models.CASCADE,
        db_column='id_direccion'
    )
    fecha_pedido = models.DateTimeField()
    estado = models.CharField(max_length=9, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor_pago = models.CharField(max_length=11, blank=True, null=True)
    referencia_pago = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'pedidos'

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.id_usuario.username}"


# ============================================================
# DETALLE DE PEDIDOS
# ============================================================

class DetallePedidos(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(
        Pedidos, models.DO_NOTHING, db_column='id_pedido'
    )
    id_producto = models.ForeignKey(
        Productos, models.DO_NOTHING, db_column='id_producto'
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedidos'

    def __str__(self):
        return f"Detalle #{self.id_detalle} - Pedido {self.id_pedido_id}"


# ============================================================
# PERFIL DE USUARIO
# ============================================================

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    preferred_contact = models.CharField(max_length=20, blank=True, null=True)
    accessibility_needs = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, 
                            choices=[("cliente", "Cliente"),
                                     ("trabajador", "Trabajador"),
                                     ("admin", "Administrador")],
                            default="cliente")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # pending / paid / canceled

    def __str__(self):
        return f"Orden #{self.id} - {self.status}"

    @property
    def total_items(self):
        """Cantidad total de unidades en la orden."""
        return sum(item.cantidad for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()

    def total(self):
        return self.cantidad * self.precio_unitario