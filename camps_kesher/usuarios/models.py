from django.db import models
from django.contrib.auth.models import User

class Fisico(models.Model):
    OBJETIVOS = [
        ("hipertrofia", "Hipertrofia"),
        ("emagrecimento", "Emagrecimento"),
        ("condicionamento", "Condicionamento Físico"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="fisico")
    data_de_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    objetivo = models.CharField(max_length=30, choices=OBJETIVOS, null=True, blank=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Fisico: {self.user.username}"
