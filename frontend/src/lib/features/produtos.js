let todosProdutos = [];

window.onload = function() {
    buscarProdutos();
    const searchInput = document.getElementById('search');

    if (searchInput) {
        searchInput.addEventListener('input', (event) => {
            filtrarProdutos(event.target.value);
        });
    } else {
        console.warn("Aviso: Elemento com ID 'search' não encontrado. A busca não funcionará.");
    }
};

function buscarProdutos() {
    fetch('http://127.0.0.1:8000/api/produtos/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede ou resposta não OK');
            }
            return response.json();
        })
        .then(data => {
            todosProdutos = data;
            exibirProdutos(todosProdutos);
        })
        .catch(error => {
            console.error('Erro ao buscar produtos:', error);
            document.getElementById('product-container').innerHTML = '<p>Não foi possível carregar os produtos. Tente novamente mais tarde.</p>';
        });
}

function filtrarProdutos(termo) {
    const termoBusca = termo.toLowerCase().trim();

    if (termoBusca === '') {
        exibirProdutos(todosProdutos);
        return;
    }

    const produtosFiltrados = todosProdutos.filter(produto => {
        return produto.nome.toLowerCase().includes(termoBusca);
    });

    exibirProdutos(produtosFiltrados);
}

function exibirProdutos(produtos) {
    const container = document.getElementById('product-container');
    container.innerHTML = '';

    if (produtos.length === 0) {
        container.innerHTML = '<p>Nenhum produto encontrado.</p>';
        return;
    }

    produtos.forEach(produto => {
        const card = document.createElement('div');
        card.className = 'product-card';
        const precoNumerico = Number(produto.preco) || 0; 
        const precoFormatado = precoNumerico.toFixed(2).replace('.', ',');
        
        card.innerHTML = `
            <div class="card">
                <a href="/frontend/src/pages/">
                    <img src="${produto.imagem}" alt="Foto de ${produto.nome}" class="product-image">
                    <h3>${produto.nome}</h3>
                    <p class="price">R$ ${precoFormatado}</p>
                </a>
            </div>
        `;

        container.appendChild(card);
    });
}

function exibirSugestoes(termo) {
    const suggestionsContainer = document.getElementById('suggestions-container');
    const termoBusca = termo.toLowerCase().trim();
    suggestionsContainer.innerHTML = ''; 

    if (termoBusca.length === 0) {
        return; 
    }
    const sugestoes = todosProdutos
        .filter(produto => produto.nome.toLowerCase().includes(termoBusca))
        .slice(0, 5); 

    sugestoes.forEach(produto => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = produto.nome;
        
        suggestionItem.addEventListener('click', () => {
            document.getElementById('search').value = produto.nome;
            filtrarProdutos(produto.nome);
            suggestionsContainer.innerHTML = ''; 
        });

        suggestionsContainer.appendChild(suggestionItem);
    });
}