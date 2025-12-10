from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Tamanho(models.Model):
    TAMANHO = [
        ("P", "Pequeno"),
        ("M", "Médio"),
        ("G", "Grande"),
        ("GG", "Extra Grande"),
        ("500ml", "500 ml"),
        ("Regulável", "Regulável"),
    ]

    nome = models.CharField(max_length=50, choices=TAMANHO)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, related_name="produtos", on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return self.nome


class ProdutoVariacao(models.Model):
    produto = models.ForeignKey(Produto, related_name="variacoes", on_delete=models.CASCADE)
    cor = models.CharField(max_length=100)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.cor} - {self.tamanho.nome}"
