from django.urls import path
from rest_tienda.views import obtener_sub

urlpatterns = [
    path('obtener_sub', obtener_sub, name="obtener_sub"),
]
