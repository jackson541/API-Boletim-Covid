from rest_framework import serializers
from .models import Caso, Cidade, Usuario, Boletim

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['id', 'nome', 'numero_habitantes', 'ativo']

class BoletimSerializer(serializers.ModelSerializer):
    casos = serializers.SerializerMethodField()

    class Meta:
        model= Boletim
        fields = ['id', 'cidade', 'data', 'casos']

    def get_casos(self, boletim):
        tipos = ['confirmado', 'tratamento', 'internado', 'recuperado', 'suspeito', 'obito', 'descartado', 'notificado']
        
        casosRelacionados = []

        for tipo in tipos:
            casosRelacionadosQuery = Caso.objects.filter(boletim=boletim.id, tipo=tipo)

            #soma o número de todos os casos filtrados
            totalNumCasos = 0
            for caso in casosRelacionadosQuery:
               totalNumCasos += caso.quantidade

            casosRelacionados.append({
                    "tipo": tipo,
                    "quantidade": totalNumCasos
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
