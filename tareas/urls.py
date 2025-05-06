# urls.py
from turtle import home
from django import views
from django.urls import path

    
from .views import  actualizar_ubicacion,agregar_empresa, agregar_informe_manejo_residuos, agregar_informe_normativas, añadir_al_carrito, buscar_por_categoria, cambiar_estado, carrito_vacio, cotizar_ubicacion,  crear_categoria, crear_ubicacion, direccion_recoleccion, editar_categoria, eliminar_categoria, eliminar_ubicacion, enviar_cotizacion, exportar_excel, exportar_pdf, historial_facturas,  home,  crear_evento, create_checkout_session, editar_evento, editar_perfil, eliminar_evento, home1, home_view, lista_categorias, listar_eventos, login_usuario, logout_usuario,  mapa_ubicaciones, mapa_ubicaciones1, mapa_ubicaciones2, mis_ubicaciones, payment_view,  registrar_gestor, registrar_usuario, resumen_co2, ver_carrito, ver_cotizaciones_recibidas, ver_perfil, ver_ruta, vista_clienteempresa, vista_clientenatural, vista_experto_ambiental, vista_gestor_residuos


urlpatterns = [
     path('', home_view, name='home'),
    path('logout/', logout_usuario, name='logout'),
    path('login/', login_usuario, name='login_usuario'), 
    path('gestor_residuos/', vista_gestor_residuos, name='vista_gestor_residuos'), 
    path('registro/gestor/', registrar_gestor, name='registrar_gestor'),
    path('experto_ambiental/', vista_experto_ambiental, name='vista_experto_ambiental'), 
    path('clienteempresa/', vista_clienteempresa, name='vista_clienteempresa'), 
    path('clientenatural/', vista_clientenatural, name='vista_clientenatural'),
    path('registro/', registrar_usuario, name='registro_usuario'),
    path('payment/', payment_view, name='payment'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('eventos/', listar_eventos, name='listar_eventos'),
    path('eventos/crear/', crear_evento, name='crear_evento'),
    path('eventos/editar/<int:id>/', editar_evento, name='editar_evento'),
    path('eventos/eliminar/<int:id>/', eliminar_evento, name='eliminar_evento'),
    path('perfil/', ver_perfil, name='ver_perfil'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('crear_ubicacion/', crear_ubicacion, name='crear_ubicacion'),
    path('mapa/', mapa_ubicaciones, name='mapa_ubicaciones'),
 path('mis_ubicaciones/', mis_ubicaciones, name='mis_ubicaciones'),
    path('editar_ubicacion/<int:pk>/', actualizar_ubicacion, name='editar_ubicacion'),
    path('eliminar_ubicacion/<int:pk>/', eliminar_ubicacion, name='eliminar_ubicacion'),
  path('buscar/', buscar_por_categoria, name='buscar_por_categoria'),
    path('resumen-co2/', resumen_co2, name='resumen_co2'),
    path('informe_manejo_residuos/nuevo/', agregar_informe_manejo_residuos, name='agregar_informe_manejo_residuos'),
    path('informe_normativas/nuevo/', agregar_informe_normativas, name='agregar_informe_normativas'),
    path('categorias/', lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', eliminar_categoria, name='eliminar_categoria'),
    path('cotizar/<int:ubicacion_id>/', cotizar_ubicacion, name='cotizar_ubicacion'),
    path('añadir_al_carrito/', añadir_al_carrito, name='añadir_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('mapa_ubicaciones1/', mapa_ubicaciones1, name='mapa_ubicaciones1'),
    path('mapa_ubicaciones2/', mapa_ubicaciones2, name='mapa_ubicaciones2'),
    path('agregar_empresa/', agregar_empresa, name='agregar_empresa'),
    
    path('historial_facturas/', historial_facturas, name='historial_facturas'),
    path('carrito_vacio/', carrito_vacio, name='carrito_vacio'),
    path('exportar-excel/', exportar_excel, name='exportar_excel'),
    path('exportar-pdf/', exportar_pdf, name='exportar_pdf'),
    path('cotizaciones/recibidas/', ver_cotizaciones_recibidas, name='ver_cotizaciones_recibidas'),
    path('enviar-cotizacion/', enviar_cotizacion, name='enviar_cotizacion'),
    path('recoleccion/<int:factura_id>/', direccion_recoleccion, name='direccion_recoleccion'),
    path('cotizaciones/<int:factura_id>/estado/<str:nuevo_estado>/', cambiar_estado, name='cambiar_estado'),
     path('cotizaciones/ruta/<int:factura_id>/', ver_ruta, name='ver_ruta'),



]

