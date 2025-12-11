window.onload = function() {
    exibirItensCarrinho();
};

const API_CART_URL = "http://127.0.0.1:8000/api/produtos/cart/";

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

function mostrarErroCarrinho(msg) {
    const container = document.getElementById('cart-container');
    if (container) {
        container.innerHTML = `<div class='cart-error' style='color:red; font-weight:bold;'>Erro: ${msg}</div>`;
    }
}

async function exibirItensCarrinho() {
    const container = document.getElementById('cart-container');
    if (!container) return;

    // Busca os itens do carrinho do backend
    const itensApi = await pegarProdutosCarrinhoDaAPI();
    let carrinho = [];
    if (itensApi.length > 0) {
        carrinho = itensApi.map(item => {
            let imagemUrl = item.imagem || '';
            if (imagemUrl && imagemUrl.startsWith('/')) {
                imagemUrl = 'http://127.0.0.1:8000' + imagemUrl;
            }

            let precoNum = typeof item.preco === 'number' ? item.preco : parseFloat(item.preco) || 0;

            return {
                id: item.variacao_id ?? item.id ?? null,
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

    console.log('Carrinho carregado:', carrinho);
    container.innerHTML = '';

    if (carrinho.length === 0) {
        container.innerHTML = '<p>Seu carrinho está vazio.</p>';
        atualizarResumo(0);
        return;
    }

    let subtotal = 0;

    carrinho.forEach((item, index) => {
        const precoValido = (item && typeof item.preco === 'number') ? item.preco : 0;
        const quantidadeValida = (item && typeof item.quantidade === 'number') ? item.quantidade : 1;
        const itemTotal = precoValido * quantidadeValida;
        subtotal += itemTotal;

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
                <button class="quantity-btn" onclick="diminuirQuantidade(${index})">-</button>
                <span class="quantidade-text" id="qtd-${index}">${quantidadeValida}</span>
                <button class="quantity-btn" onclick="aumentarQuantidade(${index})">+</button>
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

async function removerItem(index) {
    const carrinho = await pegarProdutosCarrinhoDaAPI();
    const item = carrinho[index];
    if (!item) return;

    const variacaoId = item.variacao_id ?? item.id;

    await fetch('http://127.0.0.1:8000/api/produtos/cart/remove/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ variacao_id: variacaoId })
    });

    exibirItensCarrinho();
}

async function aumentarQuantidade(index) {
    const carrinho = await pegarProdutosCarrinhoDaAPI();
    const item = carrinho[index];
    if (!item) return;

    const novaQuantidade = item.quantidade + 1;

    await fetch('http://127.0.0.1:8000/api/produtos/cart/update/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ variacao_id: item.id, quantidade: novaQuantidade })
    });

    exibirItensCarrinho();
}

async function diminuirQuantidade(index) {
    const carrinho = await pegarProdutosCarrinhoDaAPI();
    const item = carrinho[index];
    if (!item) return;

    const novaQuantidade = item.quantidade - 1;

    if (novaQuantidade <= 0) {
        return removerItem(index);
    }

    await fetch('http://127.0.0.1:8000/api/produtos/cart/update/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ variacao_id: item.id, quantidade: novaQuantidade })
    });

    exibirItensCarrinho();
}

function atualizarResumo(subtotal) {
    const subtotalEl = document.getElementById('subtotal');
    const totalEl = document.getElementById('total');
    if (subtotalEl) subtotalEl.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    if (totalEl) totalEl.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
}
