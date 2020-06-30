from rest_framework import serializers
from .models import *

class CasoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caso
        fields = ['id', 'boletim', 'tipo', 'genero', 'faixa', 'quantidade']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'user', 'criador']