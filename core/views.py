from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Perfil, Direcciones
from .forms import RegistroForm, LoginForm
from django import forms

def home(request):
    return render(request, 'home.html')

# Tienda
def tienda(request):
    return render(request, "tienda.html")

# Carrito de compras
def carrito(request):
    return render(request, "carrito.html")

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
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            # Intentar buscar por username o email
            try:
                user_obj = User.objects.get(username=identifier)
            except User.DoesNotExist:
                try:
                    user_obj = User.objects.get(email=identifier)
                except User.DoesNotExist:
                    user_obj = None

            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    if remember_me:
                        request.session.set_expiry(60 * 60 * 24 * 30)  # 30 días
                    else:
                        request.session.set_expiry(0)  # cerrar sesión al cerrar el navegador
                    return redirect('home')
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'form_login.html', {'form': form})

# Registro
def registro(request):
    if request.method == "POST":
        # --------------------------
        # DATOS DEL USUARIO
        # --------------------------
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("registro")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
            return redirect("registro")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect("registro")

        # Crear usuario Django
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # --------------------------
        # PERFIL
        # --------------------------
        # Usamos RegistroForm solo para limpiar y validar datos
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = user
            perfil.save()
        else:
            # Si algo falla en la validación del form, borramos el user creado
            user.delete()
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("registro")

        # --------------------------
        # DIRECCIÓN
        # --------------------------
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        country = request.POST.get("country")

        if street or city or state or zip_code or country:
            Direcciones.objects.create(
                id_usuario=user,
                calle=street,
                ciudad=city,
                region=state,
                codigo_postal=zip_code,
                pais=country
            )

        # --------------------------
        # LOGIN AUTOMÁTICO
        # --------------------------
        login(request, user)
        return redirect("home")

    return render(request, "form_registro.html")

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
# Agregar productor
def agregar(request):
    return render(request, "form_agregar_productos.html")

def producto(request):
    return render(request, "plantillas/producto.html")