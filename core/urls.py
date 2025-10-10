from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home.html'),
    path("tienda/", views.tienda, name="tienda"),
    path("carrito/", views.carrito, name="carrito"),
    path("chat/", views.chat, name="chat"),
    path("foro/", views.foro, name="foro"),
    path("login/", views.login_view, name="login"),
    path("registro/", views.registro, name="registro"),
    path("perfil/", views.perfil, name="perfil"),
    path("compara/", views.compara, name="compara"),
    path("publicaciones/", views.publicaciones, name="publicaciones"),
    path("agregar/", views.agregar, name="agregar"),
    path("producto/", views.producto, name="producto"),

]
