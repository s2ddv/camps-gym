from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__ (self):
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
    nome = models.CharField(max_length=20, choices=TAMANHO, unique=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="produtos")
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to="produtos/", null=True, blank=True)


    def __str__(self):
        return self.nome


class ProdutoVariacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="variacoes")
    cor = models.CharField(max_length=50)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.CASCADE)
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho.nome} - {self.cor}"         