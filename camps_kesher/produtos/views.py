import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Categoria, Tamanho, Produto, ProdutoVariacao

from .serializers import (
    CategoriaSerializer,
    ProdutoSerializer,
    TamanhoSerializer,
    ProdutoVariacaoSerializer,
    ProdutoComVariacaoSerializer
)

def get_cart(request):
    return request.session.get('cart', [])

def save_cart(request, cart):
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

class TamanhoListCreate(generics.ListCreateAPIView):
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer


class TamanhoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tamanho.objects.all()
    serializer_class = TamanhoSerializer

class ProdutoVariacaoListCreate(generics.ListCreateAPIView):
    queryset = ProdutoVariacao.objects.all()
    serializer_class = ProdutoVariacaoSerializer


class ProdutoVariacaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProdutoVariacao.objects.all()
    serializer_class = ProdutoVariacaoSerializer

class ProdutoComVariacaoCreate(generics.CreateAPIView):
    # ✅ Cria um Produto e suas Variações associadas
    serializer_class = ProdutoComVariacaoSerializer

@csrf_exempt
def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)

    data = json.loads(request.body)
    produto_id = data.get("product_id")
    cor = data.get("color")
    tamanho = data.get("size") 

    try:
        variacao = ProdutoVariacao.objects.get(
            produto_id=produto_id,
            cor=cor,
            tamanho__nome__iexact=tamanho 
        )
    except ProdutoVariacao.DoesNotExist:
        return JsonResponse({"error": "Variação não encontrada. O produto, cor ou tamanho podem estar incorretos."}, status=404)
    except ProdutoVariacao.MultipleObjectsReturned:
         return JsonResponse({"error": "Múltiplas variações encontradas. Verifique seus dados."}, status=400)

    cart = get_cart(request)

    item_existente = next(
        (item for item in cart if item['variacao_id'] == variacao.id),
        None
    )

    if item_existente:
        item_existente['quantidade'] += 1
    else:
        cart.append({
            "variacao_id": variacao.id,
            "produto": variacao.produto.nome,
            "imagem": variacao.produto.imagem.url if variacao.produto.imagem else "",
            "tamanho": variacao.tamanho.nome,
            "cor": variacao.cor,
            "preco": str(variacao.produto.preco),
            "quantidade": 1
        })
    save_cart(request, cart)
    return JsonResponse(
        {"message": f"{variacao.produto.nome} adicionado ao carrinho!"},
        status=200
    )

@csrf_exempt
def view_cart(request):
    return JsonResponse({"cart": get_cart(request)}, status=200)

@csrf_exempt
def update_cart_item(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)
    try:
        data = json.loads(request.body)
        variacao_id = data.get("variacao_id")
        quantidade = int(data.get("quantidade", 1))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Quantidade deve ser um número inteiro"}, status=400)
    cart = get_cart(request)

    item_encontrado = False
    for item in cart:
        if item.get("variacao_id") == variacao_id:
            item["quantidade"] = max(1, quantidade) 
            item_encontrado = True
            break
    
    if not item_encontrado:
        return JsonResponse({"error": "Variação ID não encontrada no carrinho"}, status=404)

    save_cart(request, cart)

    return JsonResponse({"message": "Item atualizado!"}, status=200)


@csrf_exempt
def delete_cart_item(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=405)

    try:
        data = json.loads(request.body)
        variacao_id = data.get("variacao_id")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not variacao_id:
        return JsonResponse({"error": "variacao_id é obrigatório"}, status=400)

    cart = get_cart(request)
    
    novo_cart = [item for item in cart if item.get("variacao_id") != variacao_id]
    
    if len(novo_cart) == len(cart):
        return JsonResponse({"error": "Variação ID não encontrada no carrinho"}, status=404)
    save_cart(request, novo_cart)
    return JsonResponse({"message": "Item removido!"}, status=200)

@csrf_exempt
def clear_cart(request):
    request.session["cart"] = []
    request.session.modified = True
    return JsonResponse({"message": "Carrinho limpo!"}, status=200)

class CartAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"cart": get_cart(request)})