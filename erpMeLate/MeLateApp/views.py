from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Ventas, Productos, Insumos, Proveedores, Admin

# Create your views here.

def inicio(request):
    productos = Productos.objects.all()
    cantproductos = len(productos)
    productos = productos[:3]
    listaproductos = []
    listaventas = []
    listaproveedores = []
    for producto in productos:
        listaproductos.append(producto)
    ventas = Ventas.objects.all()
    cantventas = len(ventas)
    ventas = ventas[:3]
    for venta in ventas:
        listaventas.append(venta)
    proveedores = Proveedores.objects.all()
    cantproveedores = len(proveedores)
    proveedores = proveedores[:3]
    for proveedor in proveedores:
        listaproveedores.append(proveedor)
    return render(request, 'Inicio.html', {"producto1":listaproductos[0], "producto2":listaproductos[1], "producto3":listaproductos[2], "venta1": listaventas[0], "venta2": listaventas[1], "venta3": listaventas[2],"proveedor1": listaproveedores[0], "proveedor2": listaproveedores[1], "proveedor3": listaproveedores[2],"cantidadproductos":cantproductos,"cantidadventas":cantventas, "cantidadproveedores": cantproveedores})

def ventas(request):
    ventas = Ventas.objects.all()
    productos = Productos.objects.all()
    return render(request, 'ventas.html', {"ventas": ventas, "productos":productos})

def registroVenta(request):
    formulario = request.POST.dict()
    print(formulario)
    productosventa =""
    cantidadesventa = ""
    totalventa = 0
    for llave in formulario:
        if formulario[llave] == "on":
            p = llave
            for llave1 in formulario:
                if llave1.startswith("cantidad") and llave1.find(p) != -1 and int(formulario[llave1]) > 0:
                    productosventa = productosventa + p +", "
                    cantidadesventa = cantidadesventa + formulario[llave1] +", "
                    nombre_producto = llave1[8:]
                    producto = Productos.objects.filter(nombre = nombre_producto)
                    print(producto)
                    valores_producto = producto.values()[0]
                    stockprevio = valores_producto["stock"]
                    producto.update(stock = int(stockprevio) - int(formulario[llave1]))
                    totalventa = totalventa + (int(valores_producto["precio_venta"]) * int(formulario[llave1]))
    productosventa = productosventa.strip(", ")
    cantidadesventa = cantidadesventa.strip(", ")
    print(productosventa)
    print(cantidadesventa)
    print(totalventa)
    if productosventa != "":
        nueva_venta = Ventas(productos= productosventa, cantidad = cantidadesventa, total = totalventa)
        nueva_venta.save()
    return redirect('/ventas/')

def eliminarVenta(request, id_venta):
    venta_a_eliminar = Ventas.objects.filter(id = id_venta)
    print(venta_a_eliminar)
    venta_a_eliminar.delete()
    return redirect('/ventas/')

def editarVenta(request):
    formulario = request.POST.dict()
    venta_editada = Ventas.objects.filter(id = formulario["identificacion"])
    venta_editada.update(productos= formulario["nombreproducto"], cantidad = formulario["cantidad"], total = formulario["total"])
    return redirect('/ventas/')

def insumos(request, mensaje):
    insumos = Insumos.objects.all()
    proveedores = Proveedores.objects.all()
    listaInsumos = insumos.values()
    alertas = ""
    for insumo in listaInsumos:
        medida = int(insumo["unidad_medida"][0:insumo["unidad_medida"].find(" ")])
        unidad = insumo["unidad_medida"][insumo["unidad_medida"].find(" ")+1:len(insumo["unidad_medida"])]
        if unidad == "lb":
            print(int(insumo["stock"])*medida)
            if int(insumo["stock"])*medida < 10:
                alertas = alertas + insumo["nombre"] + ", "
        if unidad == "L":
            if int(insumo["stock"])*medida < 5:
                alertas = alertas + insumo["nombre"] + ", "
        if unidad == "gr":
            if int(insumo["stock"])*medida < 5000:
                alertas = alertas + insumo["nombre"] + ", "
        if unidad == "oz":
            if int(insumo["stock"])*medida < 170:
                alertas = alertas + insumo["nombre"] + ", "
    alertas = alertas.strip(", ")
    print(alertas)
    return render(request, 'insumos.html', {"insumos": insumos, "proveedores":proveedores, "mensaje": mensaje, "alertaStock": alertas})

def registroInsumo(request):
    formulario = request.POST.dict()
    print(formulario["vencimiento"], formulario["compra"])
    fechav = formulario["vencimiento"]
    fechac = formulario["compra"]
    if(int(fechav[0:4]) < int(fechac[0:4])):
        return redirect('/insumos/fechamenor')
    elif(int(fechav[0:4]) == int(fechac[0:4])):
        if(int(fechav[5:7]) < int(fechac[5:7])):
            return redirect('/insumos/fechamenor')
        elif(int(fechav[5:7]) == int(fechac[5:7])):
            if(int(fechav[8:10]) < int(fechac[8:10])):
                return redirect('/insumos/fechamenor')
            else:
                tienestock = crearInsumo(formulario)
                if tienestock == "Bad":
                    return redirect('/insumos/imenor')
                return redirect('/insumos/actual')
        else:
            tienestock = crearInsumo(formulario)
            if tienestock == "Bad":
                return redirect('/insumos/imenor')
            return redirect('/insumos/actual')
    else:
        tienestock = crearInsumo(formulario)
        if tienestock == "Bad":
            return redirect('/insumos/imenor')
        return redirect('/insumos/actual')

def crearInsumo(formulario):
    if int(formulario["stock"]) > 0 :
        try:
            insumo_existente = Insumos.objects.filter(nombre = formulario["nombre"])
            stock = insumo_existente.values()[0]
            stock = stock["stock"]
            insumo_existente.update(stock = str(int(formulario["stock"]) + int(stock)))
        except:
            nuevo_insumo = Insumos(seccion = formulario["ubicacion"],nombre = formulario["nombre"] ,precio_compra = formulario["precio"] ,
                                stock = formulario["stock"] ,proveedor = formulario["proveedor"] ,fecha_vencimiento = formulario["vencimiento"] ,
                                fecha_ingreso = formulario["compra"] ,unidad_medida = formulario["medida"] + " " + formulario["unidad"])
            nuevo_insumo.save()
        return "Ok"
    else:
        return "Bad"

def eliminarInsumo(request, identificacion):
    insumo_a_eliminar = Insumos.objects.filter(id = identificacion)
    insumo_a_eliminar.delete()
    return redirect('/insumos/r')

def editarInsumo(request):
    formulario = request.POST.dict()
    fechav = formulario["vencimiento"]
    fechac = formulario["compra"]
    if(int(fechav[0:4]) < int(fechac[0:4])):
        return redirect('/insumos/fechamenor')
    elif(int(fechav[0:4]) == int(fechac[0:4])):
        if(int(fechav[5:7]) < int(fechac[5:7])):
            return redirect('/insumos/fechamenor')
        elif(int(fechav[5:7]) == int(fechac[5:7])):
            if(int(fechav[8:10]) < int(fechac[8:10])):
                return redirect('/insumos/fechamenor')
            else:
                tienestock = actualizarInsumo(formulario)
                if tienestock == "Bad":
                    return redirect('/insumos/imenor')
                return redirect('/insumos/actual')
        else:
            tienestock = actualizarInsumo(formulario)
            if tienestock == "Bad":
                return redirect('/insumos/imenor')
            return redirect('/insumos/actual')
    else:
        tienestock = actualizarInsumo(formulario)
        if tienestock == "Bad":
            return redirect('/insumos/imenor')
        return redirect('/insumos/actual')

def actualizarInsumo(formulario):
    insumo_editado = Insumos.objects.filter(id = formulario["identificacion"])
    if int(formulario["stock"]) > 0 :
        insumo_editado.update(seccion = formulario["ubicacion"],nombre = formulario["nombre"] ,precio_compra = formulario["precio"] ,
                                stock = formulario["stock"] ,proveedor = formulario["proveedor"] ,fecha_vencimiento = formulario["vencimiento"] ,
                                fecha_ingreso = formulario["compra"] ,unidad_medida = formulario["medida"])
        return "Ok"
    else:
        return "Bad"

def productos(request, mensaje):
    productos = Productos.objects.all()
    listaProductos = productos.values()
    alertas = ""
    for producto in listaProductos:
        if int(producto["stock"]) < 3:
            alertas = alertas + producto["nombre"] + ", "
    alertas = alertas.strip(", ")
    return render(request, 'productos.html' , {"productos": productos, "mensaje":mensaje, "alertaStock": alertas})

def registroProducto(request):
    formulario = request.POST.dict()
    print(formulario)
    fechav = formulario["vencimiento"]
    fechac = formulario["fabricacion"]
    if(int(fechav[0:4]) < int(fechac[0:4])):
        return redirect('/productos/fechamenor')
    elif(int(fechav[0:4]) == int(fechac[0:4])):
        if(int(fechav[5:7]) < int(fechac[5:7])):
            return redirect('/productos/fechamenor')
        elif(int(fechav[5:7]) == int(fechac[5:7])):
            if(int(fechav[8:10]) < int(fechac[8:10])):
                return redirect('/productos/fechamenor')
            else:
                tienestock = crearProducto(formulario)
                if tienestock == "Bad":
                    return redirect('/productos/pmenor')
                return redirect('/productos/r')
        else:
            tienestock = crearProducto(formulario)
            if tienestock == "Bad":
                return redirect('/productos/pmenor')
            return redirect('/productos/r')
    else:
        tienestock = crearProducto(formulario)
        if tienestock == "Bad":
            return redirect('/productos/pmenor')
        return redirect('/productos/r')

def crearProducto(formulario):
    if int(formulario["stock"]) > 0 :
        try:
            producto_existente = Productos.objects.filter(nombre = formulario["nombre"])
            stock = producto_existente.values()[0]
            stock = stock["stock"]
            producto_existente.update(stock = str(int(formulario["stock"]) + int(stock)))
        except:
            nuevoProducto = Productos(seccion = formulario["ubicacion"], nombre = formulario["nombre"], 
                                    precio_venta = formulario["precio"], stock = formulario["stock"], 
                                    categoria = formulario["categoria"], fecha_fabricacion = formulario["fabricacion"], 
                                    fecha_vencimiento = formulario["vencimiento"])
            nuevoProducto.save()
        return "Ok"
    else:
        return "Bad"

def eliminarProducto(request, identificacion):
    producto_a_eliminar = Productos.objects.filter(id=identificacion)
    producto_a_eliminar.delete()
    return redirect("/productos/r")

def editarProducto(request):
    formulario = request.POST.dict()
    fechav = formulario["vencimiento"]
    fechac = formulario["fabricacion"]
    if(int(fechav[0:4]) < int(fechac[0:4])):
        return redirect('/productos/fechamenor')
    elif(int(fechav[0:4]) == int(fechac[0:4])):
        if(int(fechav[5:7]) < int(fechac[5:7])):
            return redirect('/productos/fechamenor')
        elif(int(fechav[5:7]) == int(fechac[5:7])):
            if(int(fechav[8:10]) < int(fechac[8:10])):
                return redirect('/productos/fechamenor')
            else:
                tienestock = actualizarProducto(formulario)
                if tienestock == "Bad":
                    return redirect('/productos/pmenor')
                return redirect('/productos/r')
        else:
            tienestock = actualizarProducto(formulario)
            if tienestock == "Bad":
                return redirect('/productos/pmenor')
            return redirect('/productos/r')
    else:
        tienestock = actualizarProducto(formulario)
        if tienestock == "Bad":
            return redirect('/productos/pmenor')
        return redirect('/productos/r')
    return redirect('/productos/r')

def actualizarProducto(formulario):
    producto_editado = Productos.objects.filter(id = formulario["identificacion"])
    if int(formulario["stock"]) > 0 :
        producto_editado.update(seccion = formulario["ubicacion"], nombre = formulario["nombre"], 
                                    precio_venta = formulario["precio"], stock = formulario["stock"], 
                                    categoria = formulario["categoria"], fecha_fabricacion = formulario["fabricacion"], 
                                    fecha_vencimiento = formulario["vencimiento"])
        return "Ok"
    else:
        return "Bad"

def proveedores(request):
    proveedores = Proveedores.objects.all()
    return render(request, 'proveedores.html', {"proveedores": proveedores})

def registroProveedor(request):
    formulario = request.POST.dict()
    print(formulario)
    nuevoproveedor = Proveedores(nombre = formulario["nombre"], telefono = formulario["telefono"], 
                                    correo = formulario["correo"], observaciones = formulario["observaciones"])
    nuevoproveedor.save()
    return redirect('/proveedores/')

def eliminarProveedor (request, identificacion):
    proveedor_a_eliminar = Proveedores.objects.filter(id=identificacion)
    proveedor_a_eliminar.delete()
    return redirect("/proveedores/")

def editarProveedor(request):
    formulario = request.POST.dict()
    proveedor_editado = Proveedores.objects.filter(nombre = formulario["nombre"])
    proveedor_editado.update(nombre = formulario["nombre"], telefono = formulario["telefono"], 
                                    correo = formulario["correo"], observaciones = formulario["observaciones"])
    return redirect("/proveedores/")

def ingreso(request):
    formulario = request.POST.dict()
    if request.method == 'POST':
        try:
            admin = Admin.objects.get(usuario = formulario["usuario"], contrasenia = formulario["contra"])
            return redirect("/inicio/")
        except:
            return  redirect("/inicioMensaje/eautenticacion")
    return redirect("/")

def inicioDeSesion(request):
    return render(request, 'ingreso.html')

def inicioMensaje(request, mensaje):
    return render(request, 'ingreso.html', {"mensaje": mensaje})

def registroMensaje(request, mensaje):
    return render(request, 'registro.html', {"mensaje": mensaje})

def registroAdmin(request):
    formulario = request.POST.dict()
    if request.method == 'POST':
        print("entro")
        if formulario["contra"].islower() or formulario["contra"].isalpha():
            print("malo")
            return redirect("/registroMensaje/eregistro")
        else:
            print("bueno")
            nuevo_admin = Admin(usuario = formulario["usuario"], contrasenia = formulario["contra"])
            nuevo_admin.save()
            return  redirect("/inicioMensaje/correcto")
    return redirect("/registroMensaje/r")