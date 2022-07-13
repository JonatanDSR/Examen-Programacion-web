from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import Subscripcion
from django.contrib.auth.models import User
from .serializers import SubscripcionSerializer

@csrf_exempt
@api_view(['POST'])
def obtener_sub(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        id_usuario = data['id_usuario']
        try:
            user = User.objects.get(username=id_usuario)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            subscripcion = Subscripcion.objects.get(usuario=user)
        except Subscripcion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubscripcionSerializer(subscripcion)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status = status.HTTP_404_BAD_REQUEST)

@csrf_exempt
@api_view(['PUT'])
def eliminar_sub(request):
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        id_usuario = data['id_usuario']

        try:
            user = User.objects.get(username=id_usuario)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        subscripcion = Subscripcion.objects.get(usuario=user)
        subscripcion.vigencia = False
        subscripcion.save()
        
        serializer = SubscripcionSerializer(subscripcion)
        return Response(serializer.data)

