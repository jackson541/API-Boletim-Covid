from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *


class CasoList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer


class CasoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer


class UsuarioList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        #retorna apenas os usuários criados pelo admin que fez a requisição
        usuarios = Usuario.objects.filter(criador=request.user)
        serializer = UsuarioSerializer(usuarios, many=True)

        return Response(serializer.data)

    def post(self, request):
        '''
            formato de entrada:
            {
                "username": string,
                "password": string
            }
        '''
        data = JSONParser().parse(request)

        #verifica as entradas de username e password
        try:
            usuario = User.objects.create_user(username=data['username'], password=data['password'])
        
        except IntegrityError:
            return Response({'error': 'esse username já foi registrado'})
        
        except Exception:
            return Response({'error': 'valor do username ou password não informado ou incorreto'})

        data = {
            'user': usuario.id,
            'criador': request.user.id
        }
        
        serializer = UsuarioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)





