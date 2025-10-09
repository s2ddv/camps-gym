from django.shortcuts import render
from rest_framework import generics
from .models import Usuario, Fisico
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, FisicoSerializer

class UsuarioListCreate(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UsuarioCreateSerializer
        return UsuarioSerializer
class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
class FisicoListCreate(generics.ListCreateAPIView):
    queryset = Fisico.objects.all()
    serializer_class = FisicoSerializer
class FisicoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fisico.objects.all()
    serializer_class = FisicoSerializer
