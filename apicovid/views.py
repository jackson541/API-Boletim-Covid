from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

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
                "password": string,
                "cidade": number
            }
        '''
        data = JSONParser().parse(request)

        #pega todos os campos passados, transfoma em uma lista e os ordena
        keys = list(data.keys())
        keys.sort()

        camposEsperados = ['username', 'password', 'cidade']
        camposEsperados.sort()
        
        if not (keys == camposEsperados):
            return Response(
                        {'error': 'passe todos e somente os campos obrigatórios'}, 
                        status = status.HTTP_400_BAD_REQUEST
                    )

        '''
        
        
        ###################################################

        Adicionar verificação para saber se a cidade existe
        
        ###################################################
        
        
        '''

        #verifica as entradas de username e password
        try:
            usuario = User.objects.create_user(username=data['username'], password=data['password'])
        
        except IntegrityError:
            return Response(
                        {'error': 'esse username já foi registrado'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        except:
            return Response(
                        {'error': 'valor do username ou password não informado ou incorreto'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        data = {
            'user': usuario.id,
            'criador': request.user.id,
            'cidade': data['cidade']
        }
        
        serializer = UsuarioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                        {'error': f'usuário com id {pk} não encontrado'},
                        status=status.HTTP_404_NOT_FOUND
                    )

        if(usuario.criador != request.user):
            return Response(
                        {'error': 'Você não tem autorização para editar esse usuário'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

        return Response()
        



