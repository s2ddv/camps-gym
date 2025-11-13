document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    if(!id){ 
        console.error('ID não encontrado');
        return;
    }
    fetch(`http://127.0.0.1:8000/api/produtos/${id}`)
        .then(response => { 
            if (!response.ok) throw new Error('Erro ao buscar produtos');
            return response.json();
        })
        .then(data => { 
            const produto = data
            const container = document.getElementById('produto')
            container.innerHTML = '';
                const imagemUrl = `${produto.imagem}`;
                container.innerHTML = `
                <section class="main-section">
                    <div class="main-grid">
                        <div class="img-grid">
                            <div class="main-img">    
                                <div class="thumb-grid">
                                    <div class="main-thumb-grid">
                                        <img src="${imagemUrl}" alt="${produto.nome}">
                                    </div>
                                </div>
                            </div>
                        </div>
                    <div class="details-grid">
                        <p>${produto.categoria.nome}</p>
                        <h3>${produto.nome}</h3>
                        <p>R$ ${produto.preco}</p>
                        <div class="add-section"> 
                            <div class="buy-now">
                                <button id="buyBtn" class="buy-now-btn">BUY NOW</button>
                            </div>
                            <div class="add-cart">
                                <button id="cartBtn" class="cart-btn" onclick("adicionarAoCarrinho")>ADD TO CART</button>
                            </div>
                            <p>Color:</p>
                            <div class="change-color">
                                <button data-color="Preta" class="change-color-btn1"></button>
                                <button data-color="Branca" class="change-color-btn2"></button>
                                <button data-color="Azul" class="change-color-btn3"></button>
                            </div>
                            <div class="change-size">
                                <button data-size="P" class="change-size-btn1">P</button>
                                <button data-size="M" class="change-size-btn2">M</button>
                                <button data-size="G" class="change-size-btn3">G</button>
                            </div>
                            <div class="product-details">
                            
                            </div>
                        </div>
                    </div>
                </div>
        </section>
        `;

        let selectedSize = null;
        let selectedColor = null;

        document.getElementById('.change-color button').forEach(btn => { 
            btn.addEventListener('click', () => { 
                document.querySelectorAll('change-color-button').forEach(b => b.classList.remove('selected'));
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
            if(document.cookie && document.cookie !== '') { 
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) { 
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        document.getElementById('buyBtn').addEventListener('click', () => { 
            const productId = document.getElementById('buyBtn').dataset.productId;

            if (!selectedColor || !selectedSize) { 
                alert('Selecione o tamanho e a cor antes de comprar!');
                return;
            }

            fetch('/add-to-cart/', { 
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    product_id: productId,
                    color: selectedColor,
                    size: selectedSize
                })
            })
            .then(res => res.json())
            .then(data => alert(data.message))
            .catch(err => console.error(err));
        });

        document.getElementById('cartBtn').addEventListener('click', () => { 
            if (!selectedColor || selectedSize) { 
                alert('Selecione o  tamanho e a cor antes de adicionar ao carrinho!');
                return;
            }
            adicionarAoCarrinho(produto.nome, produto.preco, selectedColor, selectedSize);
        });

        function adicionarAoCarrinho(nome, preco, cor, tamanho) {
            let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

            const existente = carrinho.find(p => p.nome === nome && p.cor === cor && p.tamanho === tamanho);
            if (existente) { 
                existente.quantidade += 1;
            } else { 
                carrinho.push({ nome, preco, cor, tamanho, quantidade: 1});
            }

            localStorage.setItem('carrinho', JSON.stringify(carrinho));
            alert(`${nome} (${cor} / ${tamanho}) adicionado carrinho!`);
            }
        })
        .catch(error => { 
            console.error('Erro ao carregar produtos', error);
        });
});