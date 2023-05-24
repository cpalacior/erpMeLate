"""
URL configuration for erpMeLate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MeLateApp.views import inicioDeSesion, inicioMensaje, ingreso, registroAdmin,inicio, productos, proveedores, ventas, insumos, registroProducto, registroProducto, eliminarProducto, editarProducto, registroProveedor, eliminarProveedor, editarProveedor, registroInsumo, eliminarInsumo, editarInsumo, registroVenta, eliminarVenta, editarVenta, registroMensaje

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicioDeSesion),
    path("inicioMensaje/<mensaje>", inicioMensaje),
    path('ingreso/', ingreso),
    path('registroMensaje/<mensaje>', registroMensaje),
    path('registroAdmin/', registroAdmin),
    path('inicio/', inicio),
    path('productos/<mensaje>', productos),
    path('ventas/', ventas),  
    path('insumos/<mensaje>', insumos),     
    path('proveedores/', proveedores),
    path('registroProducto/', registroProducto),
    path('eliminarProducto/<identificacion>', eliminarProducto),
    path('editarProducto/', editarProducto),
    path('registroProveedor/', registroProveedor),
    path('eliminarProveedor/<identificacion>', eliminarProveedor),
    path('editarProveedor/', editarProveedor),
    path('registroInsumo/', registroInsumo), 
    path('eliminarInsumo/<identificacion>', eliminarInsumo),
    path('editarInsumo/', editarInsumo), 
    path('registroVenta/', registroVenta), 
    path('eliminarVenta/<id_venta>', eliminarVenta),
    path('editarVenta/', editarVenta),
]
