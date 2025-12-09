/*
 * METODOLOGIA SENAI: Este script demonstra a "Mediação da Aprendizagem".
 * O código, com seus comentários, age como um mediador, explicando
 * como o Frontend (a vitrine) "conversa" com o Backend (o almoxarifado)
 * para buscar e exibir os produtos do carrinho, tornando um conceito complexo (API REST)
 * mais acessível.
 */

// Espera o documento HTML ser completamente carregado antes de executar o script
window.onload = function() {
    exibirItensCarrinho();
};

// URL da API do carrinho
const API_CART_URL = "http://127.0.0.1:8000/api/produtos/cart/";

// Função para buscar os itens do carrinho do backend
async function pegarProdutosCarrinhoDaAPI() {
    try {
        const res = await fetch(API_CART_URL, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include'
        });
        if (!res.ok) {
            throw new Error('Erro ao buscar produtos da API: ' + res.status);
        }
        const data = await res.json();
        return Array.isArray(data.cart) ? data.cart : [];
    } catch (err) {
        mostrarErroCarrinho(err.message || err);
        return [];
    }
}

// Função para exibir mensagem de erro na tela do carrinho
function mostrarErroCarrinho(msg) {
    const container = document.getElementById('cart-container');
    if (container) {
        container.innerHTML = `<div class='cart-error' style='color:red; font-weight:bold;'>Erro: ${msg}</div>`;
    }
}

// Função principal para exibir os itens do carrinho na página
async function exibirItensCarrinho() {
    const container = document.getElementById('cart-container');
    if (!container) return;

    // Busca os itens do carrinho do backend
    const itensApi = await pegarProdutosCarrinhoDaAPI();
    let carrinho = [];
    if (itensApi.length > 0) {
        carrinho = itensApi.map(item => {
            // Corrige imagem para URL absoluta se necessário
            let imagemUrl = item.imagem || '';
            if (imagemUrl && imagemUrl.startsWith('/')) {
                imagemUrl = 'http://127.0.0.1:8000' + imagemUrl;
            }
            // Preço pode vir como string
            let precoNum = typeof item.preco === 'number' ? item.preco : parseFloat(item.preco) || 0;
            return {
                id: item.variacao_id ?? null,
                nome: item.produto ?? item.nome ?? item.title ?? 'Produto',
                imagem: imagemUrl,
                cor: item.cor ?? item.color ?? '',
                preco: precoNum,
                quantidade: typeof item.quantidade === 'number' ? item.quantidade : parseInt(item.quantidade) || 1,
                tamanho: item.tamanho ?? '',
                descricao: item.descricao ?? ''
            };
        });
    }

    console.log('Carrinho carregado:', carrinho); // Para depuração
    container.innerHTML = '';

    if (carrinho.length === 0) {
        container.innerHTML = '<p>Seu carrinho está vazio.</p>';
        atualizarResumo(0);
        return;
    }

    let subtotal = 0;

    carrinho.forEach((item, index) => {
        // Verifica se o item e o preço são válidos antes de usar
        const precoValido = (item && typeof item.preco === 'number') ? item.preco : 0;
        const quantidadeValida = (item && typeof item.quantidade === 'number') ? item.quantidade : 1;
        const itemTotal = precoValido * quantidadeValida;
        subtotal += itemTotal;

        // Estrutura do cartão do item do carrinho
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item-card';
        cartItem.innerHTML = `
            <img src="${item.imagem}" alt="${item.nome}" width="100">
            <div class="item-details">
                <h3>${item.nome}</h3>
                <p>${item.descricao || 'Descrição não disponível.'}</p>
                <div class="preco-unitario">Preço: R$ ${precoValido.toFixed(2).replace('.', ',')}</div>
                <div class="cor">Cor: ${item.cor}</div>
                <div class="tamanho">Tamanho: ${item.tamanho}</div>
            </div>
            <div class="item-quantity">
                <label for="qtd-${index}">Qtd:</label>
                <input type="number" id="qtd-${index}" value="${quantidadeValida}" min="1" data-index="${index}" onchange="atualizarQuantidade(this)">
            </div>
            <div class="item-total">
                <span>Total: R$ ${itemTotal.toFixed(2).replace('.', ',')}</span>
            </div>
            <button class="remove-item-btn" onclick="removerItem(${index})">Remover</button>
        `;
        container.appendChild(cartItem);
    });

    atualizarResumo(subtotal);
}

// Função para remover um item do carrinho (agora sincroniza com o backend)
async function removerItem(index) {
    const carrinho = await pegarProdutosCarrinhoDaAPI();
    const item = carrinho[index];
    if (!item) return;
    await fetch('http://127.0.0.1:8000/api/produtos/cart/remove/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ variacao_id: item.id })
    });
    exibirItensCarrinho();
}

// Função para atualizar a quantidade de um item do carrinho (agora sincroniza com o backend)
async function atualizarQuantidade(input) {
    const index = input.getAttribute('data-index');
    const novaQuantidade = parseInt(input.value);
    const carrinho = await pegarProdutosCarrinhoDaAPI();
    const item = carrinho[index];
    if (!item) return;
    if (novaQuantidade > 0) {
        await fetch('http://127.0.0.1:8000/api/produtos/cart/update/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ variacao_id: item.id, quantidade: novaQuantidade })
        });
        exibirItensCarrinho();
    } else {
        removerItem(index);
    }
}

// Função para atualizar o resumo do carrinho (subtotal e total)
function atualizarResumo(subtotal) {
    const subtotalEl = document.getElementById('subtotal');
    const totalEl = document.getElementById('total');
    if (subtotalEl) subtotalEl.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    if (totalEl) totalEl.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
}