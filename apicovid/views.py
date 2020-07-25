from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication \
    import TokenAuthentication, BasicAuthentication
from rest_framework import status

from .models import *
from .serializers import *


# Funções para verificação
def verificaUsuarioEAutorizacao(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)

        if not usuario.ativo:
            return Response(
                    {'error': f'usuário com id {pk} foi deletado'},
                    status=status.HTTP_404_NOT_FOUND
                )

    except ObjectDoesNotExist:
        return Response(
                    {'error': f'usuário com id {pk} não encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

    if(usuario.criador != request.user):
        return Response(
                    {'error':
                        'Você não tem autorização para editar esse usuário'},
                    status=status.HTTP_401_UNAUTHORIZED
                )


def verificaCidade(pk):
    # Verifica se a cidade existe
    try:
        cidade = Cidade.objects.get(pk=pk)

        # Verifica se a cidade já foi deletada antes
        if not cidade.ativo:
            return Response(
                    {'error': f'cidade com id {pk} foi deletada'},
                    status=status.HTTP_404_NOT_FOUND
                )

    except ObjectDoesNotExist:
        return Response(
                    {'error': f'cidade com id {pk} não encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )


def verificaBoletim(pk):
    # Verifica se o boletim existe
    try:
        boletim = Boletim.objects.get(pk=pk)

        # Verifica se o boletim já foi deletado antes
        if not boletim.ativo:
            return Response(
                    {'error': f'boletim com id {pk} foi deletado'},
                    status=status.HTTP_404_NOT_FOUND
                )

    except ObjectDoesNotExist:
        return Response(
                    {'error': f'boletim com id {pk} não encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )


# Funções para as rotas
class CidadeList(generics.ListAPIView):
    """ Retorna a lista de cidades cadastradas e ativas

    Sem parâmetros de entrada
    """

    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

    # Chamada quando o método Get faz a requisição de usuário ao DB
    def get_queryset(self):
        return Cidade.objects.filter(ativo=True)


class CidadeDetail(mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    """ Retorna uma cidade cadastrada se ela estiver ativa

    Sem parâmetros de entrada
    """

    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

    def get(self, request, *args, **kwargs):
        resposta = verificaCidade(kwargs['pk'])

        if resposta:
            return resposta

        return self.retrieve(request, *args, **kwargs)


# Usuario
class UsuarioList(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """ Retorna a lista de usuários criados pelo administrador que fez a \
        requisição

        Sem parâmetros de entrada
        """

        usuarios = Usuario.objects.filter(criador=request.user, ativo=True)
        serializer = UsuarioSerializer(usuarios, many=True)

        return Response(serializer.data)

    def post(self, request):
        """Cadastra um novo usuário se o usuário que fez a requisição tem \
        permissão de staff

        Formato de entrada:
            {
                "username": string,
                "password": string
            }
        """
        data = JSONParser().parse(request)

        # Pega todos os campos passados, transfoma em uma lista e os ordena
        keys = list(data.keys())
        keys.sort()

        camposEsperados = ['username', 'password']
        camposEsperados.sort()

        if not (keys == camposEsperados):
            return Response(
                        {'error':
                            'passe todos e somente os campos obrigatórios'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        # Verifica as entradas de username e password
        try:
            usuario = User.objects.create_user(username=data['username'],
                                               password=data['password'])

        except IntegrityError:
            return Response(
                        {'error': 'esse username já foi registrado'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        except:
            return Response(
                        {'error':
                            'valor do username ou password não informado ou incorreto'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        criador = Usuario.objects.get(user=request.user.id)

        data = {
            'user': usuario.id,
            'criador': request.user.id,
            'cidade': criador.cidade.id
        }

        serializer = UsuarioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        usuario.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioDetail(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        """ Retorna um usuário criado pelo administrador que fez a \
        requisição

        Sem parâmetros de entrada
        """

        resposta = verificaUsuarioEAutorizacao(request, pk)

        # Verifica se alguma coisa foi retornada
        if resposta:
            return resposta

        usuario = Usuario.objects.get(pk=pk)
        serializer = UsuarioSerializer(usuario)

        return Response(serializer.data)

    def put(self, request, pk):
        """ Altera todos os campos de um usuário se ele estiver ativo

        Formato de entrada:
        {
            "password": string
        }
        """

        resposta = verificaUsuarioEAutorizacao(request, pk)

        # Verifica se alguma coisa foi retornada
        if resposta:
            return resposta

        usuario = Usuario.objects.get(pk=pk)

        data = JSONParser().parse(request)

        # Pega todos os campos passados, transfoma em uma lista e os ordena
        keys = list(data.keys())
        keys.sort()

        camposEsperados = ['password']
        camposEsperados.sort()

        if not (keys == camposEsperados):
            return Response(
                        {'error':
                            'passe todos e somente os campos obrigatórios'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        criador = Usuario.objects.get(user=request.user.id)

        data = {
            'user': usuario.user.id,
            'criador': usuario.criador.id,
            'password': data['password'],
            'cidade': criador.cidade.id
        }

        # Atualiza os campos do usuário passado
        serializer = UsuarioSerializer(usuario, data=data)

        if serializer.is_valid():
            user = User.objects.get(pk=usuario.user.id)
            user.set_password(data['password'])
            user.save()

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """ Altera os campos de um usuário, mesmo que seja apenas 1, se ele \
        estiver ativo

        Formato de entrada:
        {
            "password": string
        }

        OBS: Essa rota também aceita apenas 1, ou mais, campos de entrada
        """

        resposta = verificaUsuarioEAutorizacao(request, pk)

        # Verifica se alguma coisa foi retornada
        if resposta:
            return resposta

        usuario = Usuario.objects.get(pk=pk)

        data = JSONParser().parse(request)
        cidade = usuario.cidade

        if ('password' in data):
            user = User.objects.get(pk=usuario.user.id)
            user.set_password(data['password'])
            user.save()

        data = {
            'user': usuario.user.id,
            'criador': request.user.id,
            'cidade': usuario.cidade.id
        }

        # Atualiza os campos do usuário passado
        serializer = UsuarioSerializer(usuario, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """ Inativa um usuário se ele estiver ativo

        Sem parâmetros de entrada
        """

        resposta = verificaUsuarioEAutorizacao(request, pk)

        # Verifica se alguma coisa foi retornada
        if resposta:
            return resposta

        usuario = Usuario.objects.get(pk=pk)

        serializer = UsuarioSerializer(usuario,
                                       data={'ativo': False},
                                       partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response()


# Boletim
class BoletimList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Boletim.objects.all()
    serializer_class = BoletimSerializer

    def get(self, request, *args, **kwargs):
        """ Retorna a lista de boletins cadastrados e ativos

        Sem parâmetros de entrada
        """

        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Boletim.objects.filter(ativo=True)

    def post(self, request, *args, **kwargs):
        """ Cadastra um novo boletim

        Formato de entrada:
        {
            "data": datetime,
            "casosConfirmados": int,
            "casosEmTratamento": int,
            "casosInternados": int,
            "casosRecuperados": int,
            "casosSuspeitos": int,
            "casosDeObito": int,
            "casosDescartados": int,
            "casosNotificados": int
        }
        """

        usuario = Usuario.objects.get(user=request.user.id)
        request.data['cidade'] = usuario.cidade.id

        return self.create(request, *args, **kwargs)


class BoletimDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Boletim.objects.all()
    serializer_class = BoletimSerializer

    def get(self, request, *args, **kwargs):
        """ Retorna um boletim cadastrado e ativo

        Sem parâmetros de entrada
        """

        resposta = verificaBoletim(kwargs['pk'])

        if resposta:
            return resposta

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Altera todos os campos de um boletim se ele estiver ativo

        Formato de entrada:
        {
            "data": datetime,
            "casosConfirmados": int,
            "casosEmTratamento": int,
            "casosInternados": int,
            "casosRecuperados": int,
            "casosSuspeitos": int,
            "casosDeObito": int,
            "casosDescartados": int,
            "casosNotificados": int
        }
        """

        resposta = verificaBoletim(kwargs['pk'])

        if resposta:
            return resposta

        usuario = Usuario.objects.get(user=request.user.id)
        request.data['cidade'] = usuario.cidade.id

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """ Altera os campos de um boletim, mesmo que seja apenas 1, se ele \
        estiver ativo

        Formato de entrada:
        {
            "data": datetime,
            "casosConfirmados": int,
            "casosEmTratamento": int,
            "casosInternados": int,
            "casosRecuperados": int,
            "casosSuspeitos": int,
            "casosDeObito": int,
            "casosDescartados": int,
            "casosNotificados": int
        }
        """
        resposta = verificaBoletim(kwargs['pk'])

        if resposta:
            return resposta

        usuario = Usuario.objects.get(user=request.user.id)
        request.data['cidade'] = usuario.cidade.id

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, pk):
        """ Inativa um boletim se ele estiver ativo

        Sem parâmetros de entrada
        """

        resposta = verificaBoletim(pk)

        if resposta:
            return resposta

        boletim = Boletim.objects.get(pk=pk)

        serializer = BoletimSerializer(boletim,
                                       data={'ativo': False},
                                       partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response()
