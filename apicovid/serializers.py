from rest_framework import serializers
from django.db.models import Sum
from .models import Caso, Cidade, Usuario, Boletim

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['id', 'nome', 'numero_habitantes', 'ativo']

class BoletimSerializer(serializers.ModelSerializer):
    casos = serializers.SerializerMethodField()

    class Meta:
        model= Boletim
        fields = ['id', 'cidade', 'data', 'ativo', 'casos']

    def get_casos(self, boletim):
        tipos = ['confirmado', 'tratamento', 'internado', 'recuperado', 'suspeito', 'obito', 'descartado', 'notificado']

        casosRelacionados = []

        for tipo in tipos:
            # soma os valores de 'quantidade' para casos com mesmo tipo, será 
            # retornado null se não tiver nenhum caso
            totalNumeroCasos = Caso.objects.filter(boletim=boletim.id, tipo=tipo).aggregate(Sum('quantidade'))

            casosRelacionados.append({
                    "tipo": tipo,
                    "quantidade": totalNumeroCasos['quantidade__sum'] if totalNumeroCasos['quantidade__sum'] else 0
                })

        return casosRelacionados

class CasoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caso
        fields = ['id', 'boletim', 'tipo', 'genero', 'faixa', 'quantidade', 'ativo']

class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'user', 'criador', 'cidade', 'ativo', 'username']

    def get_username(self, usuario):
        return usuario.user.username
