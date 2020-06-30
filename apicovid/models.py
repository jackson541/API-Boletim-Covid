from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .choices import *

class Caso(models.Model):
    # alterar para ForeignKey quando o model de boletim for criado
    boletim = models.IntegerField()
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='notificado')
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default='feminino')
    faixa = models.CharField(max_length=5, choices=FAIXA_CHOICES, default='0-19')
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='criador')
    cidade = models.IntegerField()
    #cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    
