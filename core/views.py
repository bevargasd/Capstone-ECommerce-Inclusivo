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
# Agregar productor
def agregar(request):
    return render(request, "form_agregar_productos.html")

def producto(request):
    return render(request, "plantillas/producto.html")