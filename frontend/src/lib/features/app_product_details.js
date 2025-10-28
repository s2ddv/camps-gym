document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    fetch(`http://127.0.0.1:8000/api/produtos/${id}/`)
        .then(response => { 
            if (!response.ok) throw new Error('Erro ao buscar produtos');
            return response.json();
        })
        .then(data => { 
            const produto = data
            const container = document.getElementById('produtos')
            container.innerHTML = '';
                const produtoDiv = document.getElementById('produto');
                produtoDiv.className = 'produto';
                const imagemUrl = `${produto.imagem}`;
                produto.innerHTML = `
                <section class="main-section">
            <div class="main-grid">
                <div class="img-grid">
                    <div class="main-img">    
                        <div class="thumb-grid">
                            <div class="main-thumb-grid">
                                <img src="${imagemUrl}" alt="${produtos.nome}">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="details-grid">
                    <p>${produtos.categoria}</p>
                    <h3>${produtos.nome}</h3>
                    <p>R$ ${produtos.preco}</p>
                    <div class="add-section"> 
                        <div class="buy-now">
                            <button class="buy-now-btn">BUY NOW</button>
                        </div>
                        <div class="add-cart">
                            <button class="cart-btn">ADD TO CART</button>
                        </div>
                        <p>Color:</p>
                        <div class="change-color">
                            <button class="change-color-btn1"></button>
                            <button class="change-color-btn2"></button>
                            <button class="change-color-btn3"></button>
                        </div>
                        <div class="change-size">
                            <button class="change-size-btn1"></button>
                            <button class="change-size-btn2"></button>
                            <button class="change-size-btn3"></button>
                            <button class="change-size-btn4"></button>
                            <button class="change-size-btn5"></button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        `;
        container.appendChild();
        })
        .catch(error => { 
            console.error('Erro ao carregar produtos', error);
        })
})
