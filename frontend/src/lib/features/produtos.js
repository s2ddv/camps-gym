// VARIÁVEL GLOBAL: Usada para armazenar a lista completa de produtos
let todosProdutos = [];

window.onload = function() {
    buscarProdutos();
    
    // 1. Adiciona o listener para o campo de busca (ID: 'search')
    const searchInput = document.getElementById('search');

    if (searchInput) {
        // Usa o evento 'input' para filtrar em tempo real conforme o usuário digita
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
            // 2. SALVA a lista completa de produtos na variável global
            todosProdutos = data;
            exibirProdutos(todosProdutos);
        })
        .catch(error => {
            console.error('Erro ao buscar produtos:', error);
            document.getElementById('product-container').innerHTML = '<p>Não foi possível carregar os produtos. Tente novamente mais tarde.</p>';
        });
}

// --- NOVA FUNÇÃO DE FILTRO ---
function filtrarProdutos(termo) {
    const termoBusca = termo.toLowerCase().trim();

    if (termoBusca === '') {
        // Se o campo estiver vazio, exibe todos os produtos
        exibirProdutos(todosProdutos);
        return;
    }

    const produtosFiltrados = todosProdutos.filter(produto => {
        // Filtra pelo nome do produto, ignorando maiúsculas/minúsculas
        return produto.nome.toLowerCase().includes(termoBusca);
    });

    exibirProdutos(produtosFiltrados);
}
// -----------------------------


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

        // Correção do TypeError: garante que produto.preco seja um número antes de usar toFixed(2)
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
    suggestionsContainer.innerHTML = ''; // Limpa as sugestões anteriores

    if (termoBusca.length === 0) {
        return; // Não mostra nada se o campo estiver vazio
    }

    // Filtra no máximo 5 sugestões
    const sugestoes = todosProdutos
        .filter(produto => produto.nome.toLowerCase().includes(termoBusca))
        .slice(0, 5); // Limita a 5 resultados

    sugestoes.forEach(produto => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion-item');
        suggestionItem.textContent = produto.nome;
        
        // Clica na sugestão e preenche o input (acionando a busca)
        suggestionItem.addEventListener('click', () => {
            document.getElementById('search').value = produto.nome;
            filtrarProdutos(produto.nome);
            suggestionsContainer.innerHTML = ''; // Esconde a lista após a seleção
        });

        suggestionsContainer.appendChild(suggestionItem);
    });
}