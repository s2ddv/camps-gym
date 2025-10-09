from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto


# 🧾 Listar produtos
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/products_list.html', {'produtos': produtos})


# ➕ Cadastrar produto (somente professor)
@login_required
def cadastrar_produto(request):
    if request.user.tipo != 'professor':  # ← validação
        return render(request, 'produtos/nao_autorizado.html', status=403)

    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_list.html')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/criar.html', {'form': form})


# ✏️ Editar produto
@login_required
def editar_produto(request, id):
    if request.user.tipo != 'professor':
        return render(request, 'produtos/nao_autorizado.html', status=403)

    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('products_list.html')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/edit_produto.html', {'form': form})


# 🗑 Excluir produto
@login_required
def excluir_produto(request, id):
    if request.user.tipo != 'professor':
        return render(request, 'produtos/nao_autorizado.html', status=403)

    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('products_list.html')
    return render(request, 'produtos/delete_produtos.html', {'produto': produto})

