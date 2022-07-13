from django.contrib import admin
from .models import Categoria, Producto, Carrito, Carrito_item, Compra, Compra_item, Subscripcion
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Carrito_item)
admin.site.register(Compra)
admin.site.register(Compra_item)
admin.site.register(Subscripcion)
