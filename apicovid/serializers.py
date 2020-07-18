from rest_framework import serializers
from django.db.models import Sum
from .models import Cidade, Usuario, Boletim


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = '__all__'


class BoletimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boletim
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'user', 'criador', 'cidade', 'ativo', 'username']

    def get_username(self, usuario):
        return usuario.user.username
