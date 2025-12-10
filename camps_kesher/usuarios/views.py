from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UsuarioSerializer, UsuarioCreateSerializer

from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


class UsuarioListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UsuarioCreateSerializer
        return UsuarioSerializer


class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer



class LoginViewAPI(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({"error": "Credenciais inválidas"}, status=400)

        login(request, user)
        return JsonResponse({"message": "Login realizado com sucesso"})


class LogoutViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logout realizado com sucesso"})


class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })
