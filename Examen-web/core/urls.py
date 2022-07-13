from django.urls import path
from . import views

app_name = "CORE"

urlpatterns = [
    path('', views.producto_index, name="producto_index"),
    path('producto/agregar', views.producto_create, name="producto_create" ),
    path('producto/<int:producto_id>', views.producto_show, name="producto_show" ),
    path('producto/<int:producto_id>/editar', views.producto_edit, name="producto_edit" ),
    path('producto/<int:producto_id>/eliminar', views.producto_delete, name="producto_delete" ),
    path('producto/buscador', views.producto_search, name="producto_search"),
    path('categoria/<int:categoria_id>/productos', views.productos_por_categoria, name="productos_por_categoria"),
    #productos
    
    path('productos', views.productos, name="producto_productos"),

    #sign up sign in
    path('registro', views.registro, name="registro"),
    path('login', views.login, name="login"),

    #carrito
    path('carrito', views.carrito_index, name="carrito_index"),
    path('carrito/agregar', views.carrito_save, name="carrito_save"),
    path('carrito/clean', views.carrito_clean, name="carrito_clean"),
    path('item_carrito/<int:item_carrito_id>/eliminar', views.item_carrito_delete, name="item_carrito_delete"),
    path('compras', views.compras, name="carrito_compras"),
    path('compras/<int:id_compra>', views.compra_con_id, name="compra_con_id"),

    #ubi
    path('ubi', views.ubicacion, name="ubicacion"),

]