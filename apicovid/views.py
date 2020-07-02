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

class CidadeList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class CidadeDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class CasoList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer


class CasoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer


#### funções para verificação
def verificaUsuarioEAutorizacao(request, pk):
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

def verificaCidade(pk):
    #verifica se a cidade existe
    try:
        cidade = Cidade.objects.get(pk = pk)

    except ObjectDoesNotExist:
        return Response(
                    {'error': f'cidade com id {pk} não encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )


#### funções para as rotas
class UsuarioList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        #retorna apenas os usuários criados pelo admin que fez a requisição
        usuarios = Usuario.objects.filter(criador=request.user)
        serializer = UsuarioSerializer(usuarios, many=True)
        
        #adiciona os usernames aos objetos retornados
        for usuario in serializer.data:
            usuario['username'] = User.objects.get(pk=usuario['user']).get_username()

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

        resposta = verificaCidade(data['cidade'])
        
        #verifica se alguma coisa foi retornada
        if not resposta == None:
            return resposta

        cidade = Cidade.objects.get(pk = data['cidade'])

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
            'cidade': cidade.id
        }
        
        serializer = UsuarioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        usuario.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        resposta = verificaUsuarioEAutorizacao(request, pk)
        
        #verifica se alguma coisa foi retornada
        if not resposta == None:
            return resposta

        usuario = Usuario.objects.get(pk=pk)

        #o serializer atual não aceita modificações nos campos
        serializer = UsuarioSerializer(usuario)
        newSerializer = serializer.data
        newSerializer['username'] = usuario.user.get_username()

        return Response(newSerializer)

    def put(self, request, pk):
        '''
            formato de entrada:
            {
                "password": string,
                "cidade": int
            }
        '''

        resposta = verificaUsuarioEAutorizacao(request, pk)
        
        #verifica se alguma coisa foi retornada
        if not resposta == None:
            return resposta

        usuario = Usuario.objects.get(pk=pk)

        data = JSONParser().parse(request)

        #pega todos os campos passados, transfoma em uma lista e os ordena
        keys = list(data.keys())
        keys.sort()

        camposEsperados = ['password', 'cidade']
        camposEsperados.sort()
        
        if not (keys == camposEsperados):
            return Response(
                        {'error': 'passe todos e somente os campos obrigatórios'}, 
                        status = status.HTTP_400_BAD_REQUEST
                    )

        resposta = verificaCidade(data['cidade'])
        
        #verifica se alguma coisa foi retornada
        if not resposta == None:
            return resposta

        cidade = Cidade.objects.get(pk = data['cidade'])

        data = {
            'user': usuario.user.id,
            'criador': usuario.criador.id,
            'password': data['password'],
            'cidade': cidade.id
        }

        #atualiza os campos do usuário passado
        serializer = UsuarioSerializer(usuario, data=data)

        if serializer.is_valid():
            user = User.objects.get(pk=usuario.user.id)
            user.set_password(data['password'])
            user.save()

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        '''
            formato de entrada:
            {
                "password": string,
                "cidade": number
            }
        '''

        resposta = verificaUsuarioEAutorizacao(request, pk)
        
        #verifica se alguma coisa foi retornada
        if not resposta == None:
            return resposta

        usuario = Usuario.objects.get(pk=pk)


        data = JSONParser().parse(request)

        #### procurar uma forma de aprimorar as verificações
        if('cidade' in data):
            resposta = verificaCidade(data['cidade'])
        
            #verifica se alguma coisa foi retornada
            if not resposta == None:
                return resposta

            cidade = Cidade.objects.get(pk = data['cidade'])

        else:
            cidade = usuario.cidade

        if ('password' in data):
            user = User.objects.get(pk=usuario.user.id)
            user.set_password(data['password'])
            user.save()

        data = {
            'user': usuario.user.id,
            'criador': request.user.id,
            'cidade': cidade.id
        }

        #atualiza os campos do usuário passado
        serializer = UsuarioSerializer(usuario, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        resposta = verificaUsuarioEAutorizacao(request, pk)
        
        #verifica se alguma coisa foi retornada
        if not resposta == None:
            return resposta

        usuario = Usuario.objects.get(pk=pk)

        usuario.user.delete()

        return Response()


