from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .choices import *

class Cidade(models.Model):
    nome = models.CharField()
    responsavel = models.ForeignKey(User)
    numero_habitantes = models.IntegerField()

class Caso(models.Model):
    # alterar para ForeignKey quando o model de boletim for criado
    boletim = models.IntegerField()
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='notificado')
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default='feminino')
    faixa = models.CharField(max_length=5, choices=FAIXA_CHOICES, default='0-19')
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])


