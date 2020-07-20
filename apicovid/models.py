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
    casosConfirmados = models.PositiveIntegerField()
    casosEmTratamento = models.PositiveIntegerField()
    casosInternados = models.PositiveIntegerField()
    casosRecuperados = models.PositiveIntegerField()
    casosSuspeitos = models.PositiveIntegerField()
    casosDeObito = models.PositiveIntegerField()
    casosDescartados = models.PositiveIntegerField()
    casosNotificados = models.PositiveIntegerField()


class Usuario(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='usuario')

    criador = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='criador')

    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True, blank=True)
