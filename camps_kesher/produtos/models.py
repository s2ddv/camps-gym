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
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="produtos")
    cor = models.CharField(max_length=50)
    tamanho = models.CharField(max_length=20, choices = Tamanho.TAMANHO)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome




