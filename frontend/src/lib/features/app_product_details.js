document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    if (!id) return console.error('ID não encontrado');

    fetch(`http://127.0.0.1:8000/api/produtos/${id}`)
        .then(res => res.json())
        .then(produto => {
            const container = document.getElementById('produto');
            container.innerHTML = `
                <section class="main-section">
                    <div class="main-grid">
                        <div class="img-grid">
                            <img src="${produto.imagem}" alt="${produto.nome}">
                        </div>
                        <div class="details-grid">
                            <p>${produto.categoria.nome}</p>
                            <h3>${produto.nome}</h3>
                            <p>R$ ${produto.preco}</p>

                            <p>Color:</p>
                            <div class="change-color">
                                <button class="change-color1" data-color="Preta">Preta</button>
                                <button class="change-color2" data-color="Branca">Branca</button>
                                <button class="change-color3" data-color="Azul">Azul</button>
                            </div>

                            <p>Size:</p>
                            <div class="change-size">
                                <button class="change-size1" data-size="P">P</button>
                                <button class="change-size2" data-size="M">M</button>
                                <button class="change-size3" data-size="G">G</button>
                            </div>

                            <button id="cartBtn" data-product-id="${produto.id}" class="cart-btn">ADD TO CART</button>
                            <button id="buyBtn" data-product-id="${produto.id}" class="buy-now-btn">BUY NOW</button>
                        </div>
                    </div>
                </section>
            `;

            let selectedColor = null;
            let selectedSize = null;

            document.querySelectorAll('.change-color button').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.change-color button').forEach(b => b.classList.remove('selected'));
                    btn.classList.add('selected');
                    selectedColor = btn.dataset.color;
                });
            });

            document.querySelectorAll('.change-size button').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.change-size button').forEach(b => b.classList.remove('selected'));
                    btn.classList.add('selected');
                    selectedSize = btn.dataset.size;
                });
            });

            function getCookie(name) {
                let cookieValue = null;
                document.cookie.split(';').forEach(cookie => {
                    cookie = cookie.trim();
                    if (cookie.startsWith(name + "=")) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    }
                });
                return cookieValue;
            }

            function addToCartAPI(productId) {
                fetch("http://127.0.0.1:8000/api/cart/add/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"  
                    },
                    body: JSON.stringify({
                        product_id: productId,
                        color: selectedColor,
                        size: selectedSize
                    })
                })
                .then(res => res.json())
                .then(data => alert(data.message || data.error))
                .catch(err => console.error(err));
            }

            document.getElementById("cartBtn").addEventListener("click", () => {
                if (!selectedColor || !selectedSize) {
                    return alert("Selecione cor e tamanho!");
                }
                addToCartAPI(produto.id);
            });

            document.getElementById("buyBtn").addEventListener("click", () => {
                if (!selectedColor || !selectedSize) {
                    return alert("Selecione cor e tamanho!");
                }
                addToCartAPI(produto.id);
                window.location.href = "/carrinho"; 
            });
        })
        .catch(err => console.error(err));
});
