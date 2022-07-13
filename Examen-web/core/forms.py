from django import forms
from django.forms import ModelForm
from .models import Producto
from django.contrib.auth.forms import UserCreationForm #nuevo
from django.contrib.auth.models import User #nuevo

#nuevo
class UserForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = ['nombreProducto', 'imagen', 'precio', 'descuento', 'stock' , 'descripcion', 'categoria']