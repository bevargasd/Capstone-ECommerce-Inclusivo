from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
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
    path("producto/<int:id>/", views.producto, name="producto"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("api/crear-orden/", views.crear_orden, name="crear_orden"),
    path("actualizar-item/<int:id>/", views.actualizar_item, name="actualizar_item"),
    path("eliminar-item/<int:id>/", views.eliminar_item, name="eliminar_item"),
    path("agregar/<int:id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("pago-completado-api/", views.pago_completado, name="pago_completado"),
    path("pago-completado/<int:id>/", views.pago_completado_page, name="pago_completado_page"),
    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),
    path("orden/<int:id>/", views.detalle_orden, name="detalle_orden"),
    path("orden/<int:id>/comprobante/", views.descargar_comprobante, name="descargar_comprobante"),

]
