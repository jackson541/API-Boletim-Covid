from rest_framework import serializers
from .models import Caso, Cidade

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['id', 'nome', 'numero_habitantes']

class CasoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caso
        fields = ['id', 'boletim', 'tipo', 'genero', 'faixa', 'quantidade']

