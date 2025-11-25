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

def view_cart(request):
    cart = get_cart(request)
    return JsonResponse({"cart": cart}, status=200)

def update_cart_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        variacao_id = data.get("variacao_id")
        quantidade = data.get("quantidade")

        cart = get_cart(request)

        for item in cart:
            if item["variacao_id"] == variacao_id:
                item["quantidade"] = quantidade
                break

        save_cart(request, cart)

        return JsonResponse({"message": "Item atualizado!"}, status=200)

    return JsonResponse({"error": "Método inválido"}, status=405)

def delete_cart_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        variacao_id = data.get("variacao_id")

        cart = get_cart(request)
        cart = [item for item in cart if item["variacao_id"] != variacao_id]

        save_cart(request, cart)

        return JsonResponse({"message": "Item removido!"}, status=200)

    return JsonResponse({"error": "Método inválido"}, status=405)

def clear_cart(request):
    request.session["cart"] = []
    return JsonResponse({"message": "Carrinho limpo"})

def remove_from_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        variacao_id = data.get("variacao_id")

        cart = request.session.get("cart", [])

        cart = [i for i in cart if i["variacao_id"] != variacao_id]

        request.session["cart"] = cart
        return JsonResponse({"message": "Item removido"})
    return JsonResponse({"error": "Método inválido"}, status=405)
