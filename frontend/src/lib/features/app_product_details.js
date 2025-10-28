document.addEventListener('DOMContentLoaded', () => {
    const categoria = document.title.split()
    fetchProdutos();
})

function fetchProdutos(){ 
    fetch('http://localhost:8000/api/produtos/')
    .then(res => res.json())
    .then(data => renderProdutos(data))
    .catch(err => console.error("Erro ao buscar produtos", err));
}

function renderProdutos(produtos){ 
    const container = document.getElementById("container");
    container.innerHTML = "";

    produtos.forEach(produtos => { 
        const card = document.createElement("div");
        card.className = "produtos";

        const imagemUrl = `http://localhost:8000/media/${produtos.imagem}`;

        card.innerHTML = `
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
        `
        container.appendChild(card);
    });
}