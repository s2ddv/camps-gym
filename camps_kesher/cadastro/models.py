from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    idade = models.PositiveIntegerField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    
     
    def __str__(self):
        return self.username
    
class Fisico(models.Model):
    OBJETIVOS= [
        ("hipertrofia", "Hipertrofia"),
        ("condicionamento", "Condicionamento Físico"),
        ("Emagrecimento", "Emagrecimento"),
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="escolher_foco")
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    foco = models.CharField(max_length=20, choices = OBJETIVOS)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.foco}"


