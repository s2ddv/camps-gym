from django.shortcuts import render
from rest_framework import generics
from .models import Usuario, Fisico
from .serializers import UsuarioSerializer, UsuarioCreateSerializer,FisicoSerializer, ChangePasswordSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


Usuario = get_user_model()

def cadastro(request): 
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else: 
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        return HttpResponse(email)
def login(request):
    return render(request, 'login.html')

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
@login_required
def cadastrar_produto(request):
    # Apenas professores podem cadastrar produtos
    if request.user.tipo != 'professor':
        return render(request, 'produtos/nao_autorizado.html', status=403)

    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'products_list.html')
    else:
        form = ProdutoForm()

    return render(request, 'produtos/crud_produtos.html', {'form': form})