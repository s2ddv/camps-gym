import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from .models import Categoria, Tamanho, Produto, ProdutoVariacao
from .serializers import CategoriaSerializer, ProdutoSerializer

def get_cart(request):
    """Retorna o carrinho da sessão ou cria um novo"""
    return request.session.get('cart', [])


def save_cart(request, cart):
    """Salva o carrinho atualizado na sessão"""
    request.session['cart'] = cart
    request.session.modified = True

class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

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

        # Busca variação do produto
        try:
            variacao = ProdutoVariacao.objects.get(
                produto_id=produto_id,
                cor=cor,
                tamanho__nome=tamanho
            )
        except ProdutoVariacao.DoesNotExist:
            return JsonResponse({"error": "Variação não encontrada"}, status=404)

        cart = get_cart(request)

        item_existente = next((item for item in cart if item['variacao_id'] == variacao.id), None)

        if item_existente:
            item_existente['quantidade'] += 1
        else:
            cart.append({
                "variacao_id": variacao.id,
                "produto": variacao.produto.nome,
                "tamanho": variacao.tamanho.nome,
                "cor": variacao.cor,
                "preco": str(variacao.produto.preco),
                "quantidade": 1
            })

        save_cart(request, cart)

        return JsonResponse({"message": f"{variacao} adicionado ao carrinho!"}, status=200)

    return JsonResponse({"error": "Método inválido"}, status=405)
