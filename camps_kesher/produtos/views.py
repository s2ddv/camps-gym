import json
from django.shortcuts import render
from .models import ProdutoVariacao
from django.http import JsonResponse
from rest_framework import generics
from .models import Categoria, Tamanho, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer

class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer = CategoriaSerializer
class ProdutoListCreate(generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
class ProdutoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        produto_id = data.get("product_id")
        cor = data.get("color")
        tamanho = data.get("size")

        try: 
            variacao = ProdutoVariacao.objects.get(produto_id=produto_id, cor=cor, tamanho__nome=tamanho)
        except ProdutoVariacao.DoesNotExist: 
            return JsonResponse({"error": "Variação não encontrada"}, status=404)

        request.session.setdefault('cart', [])
        request.session['cart'].append({
            "produto": variacao.produto.nome,
            "tamanho": variacao.tamanho.nome,
            "cor": variacao.cor,
        })
        request.session.modified = True

        return JsonResponse({"message": f"{variacao} adicionado ao carrinho!"})
        
    return JsonResponse({"error": "Método inválido"}, status=405)
