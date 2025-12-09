from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Order, OrderItem, Perfil, Direcciones, Productos, Categoria
from .forms import RegistroForm, LoginForm, ProductoForm
from django import forms
from django.db.models import Q
from django.utils import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas


def home(request):
    productos = Productos.objects.all() 
    return render(request, "home.html", {"productos": productos})

# Tienda
def tienda(request):
    categorias = Categoria.objects.all()
    productos = Productos.objects.all()

    return render(request, 'tienda.html', {
        'categorias': categorias,
        'productos': productos
    })

# Carrito de compras
def carrito(request):

    if not request.user.is_authenticated:
        return redirect("login")

    # Buscar la orden pendiente o crear una nueva
    order, created = Order.objects.get_or_create(
        user=request.user,
        status="pending",
        defaults={"total": 0}
    )

    # Recalcular el total
    order.total = sum(item.total() for item in order.items.all())
    order.save()

    return render(request, "carrito.html", {
        "order": order,
        "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID
    })

# Chatbot
def chat(request):
    return render(request, "chat.html")

# Foro
def foro(request):
    return render(request, "foro.html")

# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier'].strip().lower()
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            # Intentar buscar por username o email
            try:
                user_obj = User.objects.get(username__iexact=identifier)
            except User.DoesNotExist:
                try:
                    user_obj = User.objects.get(email__iexact=identifier)
                except User.DoesNotExist:
                    user_obj = None

            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    if remember_me:
                        request.session.set_expiry(60 * 60 * 24 * 30)
                    else:
                        request.session.set_expiry(0)
                    return redirect('home')

            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'form_login.html', {'form': form})

# Registro
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("registro")
    else:
        form = RegistroForm()
    return render(request, "form_registro.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    return redirect("home")


def cerrar_sesion(request):
    logout(request)
    return redirect("home")


def perfil(request):
    return render(request, "plantillas/perfil.html")

# Comparador de productos
def compara(request):
    return render(request, "compara.html")

# Publicaciones
def publicaciones(request):
    return render(request, "publicacion.html")
# Agregar productos

def agregar(request):
    categorias = Categoria.objects.all()

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save(commit=False)
            producto.fecha_creacion = timezone.now()
            producto.activo = True
            producto.save()

            messages.success(request, "Producto agregado correctamente.")

        else:
            messages.error(request, "Revisa los campos del formulario.")

    else:
        form = ProductoForm()

    return render(request, "form_agregar_productos.html", {
        "form": form,
        "categorias": categorias,
    })

def producto(request, id):
    try:
        producto = Productos.objects.get(id_producto=id)
    except Productos.DoesNotExist:
        raise Http404("Producto no encontrado")

    imagenes = []
    if producto.imagen_uno:
        imagenes.append(producto.imagen_uno.url)
    if producto.imagen_dos:
        imagenes.append(producto.imagen_dos.url)

    return render(request, "plantillas/producto.html", {
        "producto": producto,
        "imagenes": imagenes
    })

@csrf_exempt
def crear_orden(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)

    items = data.get("items", [])
    user_id = data.get("user_id", None)

    if not items:
        return JsonResponse({"error": "Carrito vacío"}, status=400)

    # ============= VALIDACIONES =============
    total_real = 0
    productos_validos = []

    for item in items:
        try:
            p = Productos.objects.get(id_producto=item["id"])
        except Productos.DoesNotExist:
            return JsonResponse({"error": f"Producto {item['id']} no existe"}, status=400)

        cantidad = int(item["cantidad"])

        if cantidad <= 0:
            return JsonResponse({"error": "Cantidad inválida"}, status=400)

        total_real += p.precio * cantidad

        productos_validos.append({
            "producto": p,
            "cantidad": cantidad,
            "precio": p.precio
        })

    # ============= CREAR LA ORDEN =============
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total=total_real
    )

    # Crear items
    for item in productos_validos:
        OrderItem.objects.create(
            order=order,
            producto=item["producto"],
            cantidad=item["cantidad"],
            precio_unitario=item["precio"]
        )

    return JsonResponse({
        "message": "Orden creada correctamente",
        "order_id": order.id,
        "total": total_real
    })


def actualizar_item(request, id):
    item = OrderItem.objects.get(id=id)
    item.cantidad = int(request.POST["cantidad"])
    item.save()

    # actualizar total
    order = item.order
    order.total = sum(i.total() for i in order.items.all())
    order.save()

    return redirect("carrito")


def eliminar_item(request, id):
    item = OrderItem.objects.get(id=id)
    order = item.order
    item.delete()

    order.total = sum(i.total() for i in order.items.all())
    order.save()

    return redirect("carrito")

@csrf_exempt
def pago_completado(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Método no permitido"}, status=405)

    data = json.loads(request.body)
    paypal_order_id = data.get("paypal_order_id")

    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "Usuario no autenticado"}, status=403)

    try:
        order = Order.objects.get(user=request.user, status="pending")
    except Order.DoesNotExist:
        return JsonResponse({"ok": False, "error": "No existe una orden pendiente"}, status=404)

    # Marcar como pagada
    order.status = "paid"
    order.paypal_id = paypal_order_id
    order.save()

    return JsonResponse({
        "ok": True,
        "order_id": order.id
    })


def pago_completado_page(request, id):
    order = get_object_or_404(Order, id=id)

    if order.user != request.user:
        return HttpResponse("No tienes permiso para ver esta orden.", status=403)

    return render(request, "pago_completado.html", {
        "order": order
    })


def mis_pedidos(request):
    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(user=request.user, status="paid").order_by("-created_at")

    return render(request, "mis_pedidos.html", {
        "orders": orders
    })

def detalle_orden(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)

    return render(request, "detalle_orden.html", {
        "order": order
    })

def descargar_comprobante(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)

    # Respuesta como PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="orden_{order.id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"Comprobante de Pago - Orden #{order.id}")
    p.drawString(100, 780, f"Fecha: {order.created_at.strftime('%d/%m/%Y')}")
    p.drawString(100, 760, f"Estado: {order.status}")
    p.drawString(100, 740, f"Total: ${order.total}")

    y = 700
    p.setFont("Helvetica", 12)
    p.drawString(100, y, "Productos:")
    y -= 20

    for item in order.items.all():
        p.drawString(120, y, f"- {item.producto.nombre} x{item.cantidad} = ${item.total()}")
        y -= 20

    p.showPage()
    p.save()

    return response


def agregar_al_carrito(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    producto = get_object_or_404(Productos, id_producto=id)

    # Obtener o crear orden pendiente
    order, created = Order.objects.get_or_create(
        user=request.user,
        status="pending",
        defaults={"total": 0}
    )

    # Buscar si el producto ya está en el carrito
    item, item_created = OrderItem.objects.get_or_create(
        order=order,
        producto=producto,
        defaults={
            "cantidad": 1,
            "precio_unitario": producto.precio
        }
    )

    if not item_created:
        item.cantidad += 1
        item.save()

    # Recalcular total
    order.total = sum(i.total() for i in order.items.all())
    order.save()

    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect("carrito")