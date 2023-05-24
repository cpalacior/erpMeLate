from django.db import models

# Create your models here.
class Productos(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    seccion = models.CharField(max_length=45, unique=False, null=False)
    nombre = models.CharField(max_length=20, unique=False, null=False)
    precio_venta = models.IntegerField(null=False, unique=False)
    stock = models.IntegerField(null=False, unique=False)
    categoria = models.CharField(max_length=20, unique=False, null=False)
    fecha_fabricacion = models.DateField(auto_now=False, auto_now_add=False)
    fecha_vencimiento = models.DateField(auto_now=False, auto_now_add=False)

class Ventas(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    productos = models.CharField(max_length=100, unique=False, null=False)
    cantidad = models.CharField(max_length=50, unique=False, null=False)
    total = models.IntegerField(null=False, unique=False)

class Insumos(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    seccion = models.CharField(max_length=45, unique=False, null=False)
    nombre = models.CharField(max_length=20, unique=False, null=False)
    precio_compra = models.IntegerField(null=False, unique=False)
    stock = models.IntegerField(null=False, unique=False)
    proveedor = models.CharField(max_length=45, unique=False, null=False)
    fecha_vencimiento = models.DateField(auto_now=False, auto_now_add=False)
    fecha_ingreso = models.DateField(auto_now=False, auto_now_add=False)
    unidad_medida = models.CharField(max_length=20, unique=False, null=False)

class Proveedores(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=45, unique=False, null=False)
    telefono = models.BigIntegerField(null=False, unique=False)
    correo = models.CharField(max_length=45, unique=False, null=False)
    observaciones = models.CharField(max_length=100, unique=False, null=False)

class Admin(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    usuario = models.CharField(max_length=20, unique=False, null=False)
    contrasenia = models.CharField(max_length=20, unique=False, null=False)