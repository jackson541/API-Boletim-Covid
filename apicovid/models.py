from django.db import models
from .choices import *

class Caso(models.Model):
    # alterar para ForeignKey quando o model de boletim for criado
    boletim = models.IntegerField()
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='notificado')
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default='feminino')
    faixa = models.CharField(max_length=5, choices=FAIXA_CHOICES, default='0-19')
    
