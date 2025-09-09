from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



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
    return render(request, "form_login.html")

# Registro
def registro(request):
    return render(request, "form_registro.html")

# Perfil
def perfil(request):
    return render(request, "perfil.html")

# Comparador de productos
def compara(request):
    return render(request, "compara.html")

# Publicaciones
def publicaciones(request):
    return render(request, "publicacion.html")