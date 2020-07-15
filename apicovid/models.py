from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .choices import *


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    numero_habitantes = models.IntegerField()
    ativo = models.BooleanField(default=True, blank=True)


class Boletim(models.Model):
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    data = models.DateTimeField()
    ativo = models.BooleanField(default=True, blank=True)


class Caso(models.Model):
    boletim = models.ForeignKey(Boletim, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15,
                            choices=TIPO_CHOICES,
                            default='notificado')

    genero = models.CharField(max_length=10,
                              choices=GENERO_CHOICES,
                              default='feminino')

    faixa = models.CharField(max_length=5,
                             choices=FAIXA_CHOICES,
                             default='0-19')

    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    ativo = models.BooleanField(default=True, blank=True)


class Usuario(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='usuario')

    criador = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='criador')

    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True, blank=True)
