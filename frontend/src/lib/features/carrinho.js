// Espera o documento carregar para executar o script
window.onload = function() {
    exibirItensCarrinho();
};

function exibirItensCarrinho() {
    const container = document.getElementById('cart-container');
    const carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

    container.innerHTML = ''; // Limpa o container

    if (carrinho.length === 0) {
        container.innerHTML = '<p>Seu carrinho está vazio.</p>';
        atualizarResumo(0);
        return;
    }

    let subtotal = 0;

    carrinho.forEach((item, index) => {
        // **MELHORIA AQUI**: Verificamos se o item e o preço são válidos antes de usar
        const precoValido = (item && typeof item.preco === 'number') ? item.preco : 0;
        const quantidadeValida = (item && typeof item.quantidade === 'number') ? item.quantidade : 1;

        const itemTotal = precoValido * quantidadeValida;
        subtotal += itemTotal;

        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item-card';
        cartItem.innerHTML = `
            <div id="card-items-container">
                    <img src="${produto.imagem}" alt="Foto de ${produto.nome}" style="width: 200px; height: 250px;>
                    <div class="container-informations-item">
                        <h5>${produto.nome}</h5>
                        <h6>EDIÇÃO PADRÃO</h6>
                        <div class="container-color">
                            <h4>COLOR:</h4>
                            <div class="box-color">${produto.cor}</div>
                        </div>
                    </div>
                    <div class="container-quantity">
                        <h5>QUANTIDADE</h5>
                        <button class="btn-less-quantity" data-index="0">-</button> <!-- Identifica o índice do item -->
                        <div class="container-quantity-number">1</div>
                        <button class="btn-more-quantity" data-index="0">+</button>
                    </div>
                    <div class="container-value">
                        <p class="value-items">R$ 15,00</p>
                    </div>
                    <div class="container-remove">
                        <button class="btn-remove-item">REMOVER</button>
                    </div>
                </div>
                
                <div class="container-finalization">
                    <div class="container-promotion">
                        <p class="title-promo-code">TEM UM CÓDIGO DE PROMOÇÃO?</p>
                        <div class="box-text-aplicate">
                        <input type="text" id="promo-code" class="input-promo-code" name="promo-code">
                        <button class="btn-aplicar-codigo">APLICAR</button>
                        </div>
                    </div>
                    <div class="container-items-total">
                        <div class="box-items">
                            <p class="items-frete">1 ITEM(S) SUBTOTAL</p>
                            <p class="items-frete">70R$</p>
                        </div>
                        <div class="box-frete">
                            <p class="items-frete">FRETE<p>
                            <p class="items-frete">N/A</p>
                        </div>
                        <div class="box-price-total">
                            <p class="total-price">VALOR TOTAL</p>
                            <p class="total-price">70R$</p>
                        </div>
                        <div class="box-btn-clean-whatsapp">
                            <button id="limpar-pedido" class="btn">
                                <img src="/frontend/src/assets/icon - lixo.png" style="width: 50px;">
                            </button>
                            <button id="checkout-btn" class="btn">
                                <img src="/frontend/src/assets/icon - whatsapp.png" style="width: 50px;">
                            </button>
                        </div>
                    </div>
                    
                </div>
        `;
        container.appendChild(cartItem);
    });

    atualizarResumo(subtotal);
}

function removerItem(index) {
    let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];
    carrinho.splice(index, 1);
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
    exibirItensCarrinho();
}



// Função que atualiza o carrinho no localStorage
function atualizarQuantidade(input) {
  const index = input.getAttribute('data-index');
  const novaQuantidade = parseInt(input.value);
  let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

  if (carrinho[index]) {
    if (novaQuantidade > 0) {
      carrinho[index].quantidade = novaQuantidade;
      localStorage.setItem('carrinho', JSON.stringify(carrinho));
      exibirtItensCarrinho(); // se você tiver essa função
    } else {
      removerItem(index);
    }
  }
}

// ---- 🔽 Essa parte vai FORA da função acima ----

// Botão de diminuir quantidade
document.querySelectorAll('.btn-less-quantity').forEach(button => {
  button.addEventListener('click', function() {
    const index = this.getAttribute('data-index');
    let quantidade = parseInt(document.querySelector(`.container-quantity-number[data-index="${index}"]`).innerText);
    if (quantidade > 1) {
      quantidade--;
      document.querySelector(`.container-quantity-number[data-index="${index}"]`).innerText = quantidade;
      atualizarQuantidade({ value: quantidade, getAttribute: () => index });
    }
  });
});

// Botão de aumentar quantidade
document.querySelectorAll('.btn-more-quantity').forEach(button => {
  button.addEventListener('click', function() {
    const index = this.getAttribute('data-index');
    let quantidade = parseInt(document.querySelector(`.container-quantity-number[data-index="${index}"]`).innerText);
    quantidade++;
    document.querySelector(`.container-quantity-number[data-index="${index}"]`).innerText = quantidade;
    atualizarQuantidade({ value: quantidade, getAttribute: () => index });
  });
});

function atualizarResumo(subtotal) {
    const subtotalEl = document.getElementById('subtotal');
    const totalEl = document.getElementById('total');

    subtotalEl.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    totalEl.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
}