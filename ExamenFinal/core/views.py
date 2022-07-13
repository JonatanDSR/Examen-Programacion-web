from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http.response import HttpResponse
from .models import Producto
from .forms import ProductoForm
from core.models import *
from django.contrib.auth.forms import UserCreationForm #nuevo
from django.contrib.auth.models import User #nuevo
from django.contrib import messages #nuevo
# Create your views here.
def home(request):

	return render(request, 'core/home.html')

def productos(request):

    return render(request, 'core/producto/productos.html')

def login(request):

	return render(request, 'registration/login.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            usuario_logeado = User.objects.last()
            messages.success(request, f"El usuario ha sido registrado exitosamente!")
            carrito = Carrito()
            carrito.usuario = usuario_logeado
            carrito.total = 0
            carrito.save()

            subscripcion = Subscripcion()
            subscripcion.usuario = usuario_logeado
            subscripcion.vigencia = False
            subscripcion.save()

            return redirect(to="CORE:producto_index")
        else:
            messages.success(request, "Registro fallido. Favor reintentar")

    return render(request, 'registration/register.html')

def producto_index(request):
    productos = Producto.objects.all().order_by("-idProducto")
    
    return render(request, "core/producto/index.html", {
        'categorias' : Categoria.objects.all(),
        #'productos' : productos[3:10] codigo para obtener solo algunos
        'productos' : productos
    })

def producto_create(request):
    categorias = Categoria.objects.all()
    if request.method == "POST":
        categoria_del_producto = Categoria.objects.get(idCategoria=request.POST["categoria"])
        form = ProductoForm(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen'], categoria=categoria_del_producto))   
        if form.is_valid():
            form.save()
            return redirect("CORE:producto_productos")
        else:
            return render(request, 'core/producto/create.html', {
                'categorias' : categorias,
                'error_message' : 'Ingreso un campo incorrecto, vuelva a intentar'
            })
    else:
        return render(request, 'core/producto/create.html', {
            'categorias' : categorias
        })

def producto_show(request, producto_id):
    producto =  get_object_or_404(Producto, idProducto=producto_id)

    return render(request, 'core/producto/show.html',{
        'categorias' : Categoria.objects.all(),
        'producto' : producto
    })

def producto_edit(request, producto_id):
    categorias = Categoria.objects.all()
    producto = get_object_or_404(Producto, idProducto=producto_id)

    if request.method == "POST":
        categoria_del_producto = Categoria.objects.get(idCategoria=request.POST["categoria"])
        form = ProductoForm(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen'], categoria=categoria_del_producto))   
        if form.is_valid():
            producto.nombreProducto = request.POST['nombreProducto']
            producto.categoria = categoria_del_producto
            producto.descripcion = request.POST['descripcion']
            producto.imagen = request.FILES['imagen']
            producto.precio = request.POST['precio']
            producto.descuento = request.POST['descuento']
            producto.stock = request.POST['stock']
            producto.save()
            return redirect("CORE:producto_productos")
        else:
            return render(request, 'core/producto/edit.html', {
                'categorias' : categorias,
                'error_message' : 'Ingreso un campo incorrecto, vuelva a intentar'
            })
    else:
        return render(request, 'core/producto/edit.html',{
            'categorias' : categorias,
            'producto' : producto
        })

def producto_delete(request, producto_id):
    producto = Producto.objects.get(idProducto=producto_id)
    producto.delete()
    return redirect('CORE:producto_index')

def producto_search(request):
    texto_de_busqueda = request.GET["texto"]
    productosPorTitulo = Producto.objects.filter(nombreProducto__icontains = texto_de_busqueda).all()
    productosPorDescripcion = Producto.objects.filter(descripcion__icontains = texto_de_busqueda).all()
    productos = productosPorTitulo | productosPorDescripcion 
    return render(request, 'core/producto/search.html',
    {
        'categorias' : Categoria.objects.all(),
        'productos' : productos
    })
  
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, idCategoria = categoria_id)
    productos = categoria.productos.all()
    return render(request, 'core/producto/search.html',
    {
        'categorias' : Categoria.objects.all(),
        'productos' : productos,
        'categoria' : categoria.nombreCategoria,
    })

#funciones para el carrito

def carrito_index(request):
    categorias = Categoria.objects.all()
    usuario_logeado = User.objects.get(username=request.user)
    productos = Carrito.objects.get(usuario=usuario_logeado.id).items.all()

    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    nuevo_precio_Carrito = 0
    for item in carrito.items.all():
        #validar si es que tiene descuento
        nuevo_precio_Carrito += (item.producto.precio - (item.producto.precio * item.producto.descuento/100))

    carrito.total = nuevo_precio_Carrito
    carrito.save()
    precio = nuevo_precio_Carrito
    if request.method == 'POST':
        compra = Compra()
        compra.usuario = usuario_logeado
        compra.total = carrito.total
        compra.estado = 'Compra realizada!'
        compra.save()

        for item in carrito.items.all():
            producto = Producto.objects.get(idProducto=item.producto.idProducto)
            items_compra = Compra_item()
            items_compra.compra = compra
            items_compra.producto = producto
            items_compra.save()

        for item in carrito.items.all():
            producto = Producto.objects.get(idProducto=item.producto.idProducto)
            producto.stock = producto.stock - 1
            producto.save()
        
        carrito.items.all().delete()
        carrito.total = 0
        carrito.save()

        messages.success(request, f"Compra realizada con exito!")

        return redirect('CORE:producto_index')

    return render(request, 'core/carrito/index.html', {
        'categorias' : categorias,
        'usuario' : usuario_logeado,
        'items_carrito' : productos,
        'carrito' : carrito,
        'newprice' : precio
         
    })

def carrito_save(request):

    if request.method == 'POST':
        producto = Producto.objects.get(idProducto=request.POST['producto_id'])
        usuario_logeado = User.objects.get(username=request.user)

        #Agregamos el producto
        carrito = Carrito.objects.get(usuario=usuario_logeado.id)
        item_carrito = Carrito_item()
        item_carrito.carrito = carrito
        item_carrito.producto = producto
        item_carrito.save()

        #Sumamos el precio
        carrito.total = producto.precio + carrito.total
        carrito.save()
        messages.success(request, f"El producto {producto.nombreProducto} fue agregado al carrito")
        return redirect("CORE:producto_productos")

    else:
        return redirect("CORE:producto_index")

def carrito_clean(request):
    usuario_logeado = User.objects.get(username=request.user)
    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    carrito.items.all().delete()
    carrito.total = 0
    carrito.save()
    return redirect('CORE:carrito_index')

def item_carrito_delete(request, item_carrito_id):
    item_carrito = Carrito_item.objects.get(id=item_carrito_id)
    carrito = item_carrito.carrito
    
    nuevo_precio_Carrito = 0 - item_carrito.producto.precio
    for item in carrito.items.all():
        nuevo_precio_Carrito += item.producto.precio

    carrito.total = nuevo_precio_Carrito
    item_carrito.delete()
    carrito.save()
    return redirect("CORE:carrito_index")


def compras (request):
    usuario_logeado = User.objects.get(username=request.user)
    compras = usuario_logeado.compras.all()

    return render(request, "core/carrito/compras.html",
    { 'compras' : compras })

def compra_con_id (request, id_compra):
    productos = Compra.objects.get(id=id_compra).items_compra.all()
    return render(request, 'core/carrito/compra_mostrar.html', 
    { 'productos': productos })

def ubicacion (request):

    return render(request, 'core/producto/ubicacion.html')
