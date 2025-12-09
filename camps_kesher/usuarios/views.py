from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UsuarioSerializer, UsuarioCreateSerializer

class UsuarioListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UsuarioCreateSerializer
        return UsuarioSerializer

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
