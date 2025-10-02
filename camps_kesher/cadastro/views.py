from django.shortcuts import render
from rest_framework import generics
from .models import Usuario, Fisico
from .serializers import UsuarioSerializer, UsuarioCreateSerializer,FisicoSerializer, ChangePasswordSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioListCreate(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UsuarioCreateSerializer
        return UsuarioSerializer
class UsuarioDetail(generics.RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class FisicoListCreate(generics.ListCreateAPIView):
    queryset = Fisico.objects.all()
    serializer_class = FisicoSerializer
class FisicoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fisico.objects.all()
    serializer_class = FisicoSerializer
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UsuarioCreateSerializer
        return UsuarioSerializer

    # 🔹 rota customizada: /usuarios/{id}/change-password/
    @action(detail=True, methods=["post"], url_path="change-password")
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": "Senha antiga incorreta"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"status": "senha alterada com sucesso ✅"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)