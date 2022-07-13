from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name='Id de categoria')
    nombreCategoria = models.CharField(max_length=50, verbose_name='Nombre de la Categoria')

    def __str__(self):
        return self.nombreCategoria

class Producto(models.Model):
    idProducto = models.AutoField(primary_key = True, verbose_name='Id del producto')
    nombreProducto = models.CharField(max_length=30)
    imagen = models.FileField(upload_to='productos/')
    precio = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    descuento = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    descripcion = models.CharField(max_length=500, null=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name="productos")

    def __str__(self):
        return self.nombreProducto

class Carrito(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Id de carrito')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    total = models.DecimalField(null=False, max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Id: {self.id} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"


class Carrito_item(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Id de Item carrito')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return f"Id: {self.id} | Producto: {self.producto.nombreProducto} | Carrito_id: {self.carrito.id}"

class Compra(models.Model):
    #id = models.IntegerField(primary_key=True, verbose_name='Id de compra')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compras")
    total = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return f"Id: {self.pk} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total} | Estado:{self.estado}" 

class Compra_item(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="items_compra")

    def __str__(self) -> str:
        return f"Id: {self.pk} | Producto: {self.producto.nombreProducto} | compra_id: {self.compra.id}"

class Subscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscripcion")
    vigencia = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Id: {self.pk} | usuario_id: {self.usuario.id} | usuario: {self.usuario.username} | vigencia: {self.vigencia}"
