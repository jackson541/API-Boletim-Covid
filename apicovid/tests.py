from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Cidade, Usuario, Caso

'''
    OBS: o Django cria um db separado para os testes
'''

class UsuarioTeste(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='teste', password='teste', is_staff=True)
        self.cidade = Cidade.objects.create(nome="cidadeTeste", numero_habitantes=10)

        #força autenticação para não precisa do token
        self.client.force_authenticate(user=self.user)

        ## usuários padrões para teste
        user1 = User.objects.create(username='testeListagem1', password='teste')
        user2 = User.objects.create(username='testeListagem2', password='teste')
        user3 = User.objects.create(username='testeListagem3', password='teste')
        user4 = User.objects.create(username='testeListagem4', password='teste')

        self.usuario1 = Usuario.objects.create(user=user1, criador=self.user, cidade=self.cidade)
        self.usuario2 = Usuario.objects.create(user=user2, criador=self.user, cidade=self.cidade)
        self.usuario2 = Usuario.objects.create(user=user3, criador=self.user, cidade=self.cidade)
        self.usuario2 = Usuario.objects.create(user=user4, criador=self.user, cidade=self.cidade)
        
    ### GET
    def test_listar_usuarios(self):
        url = reverse("list_create_usuario")

        NUM_CASOS_LISTADOS = 4

        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), NUM_CASOS_LISTADOS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_listar_um_usuario(self):
        USUARIO_ID = 2
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        RESPOSTA_ESPERADA = {'id': 2, 'user': 3, 'criador': 1, 'cidade': 1, 'ativo': True, 'username': 'testeListagem2'}

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_listar_um_usuario_negado(self):
        USUARIO_ID = 20
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        RESPOSTA_ESPERADA = {'error': 'usuário com id 20 não encontrado'}

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    ### POST
    def test_criar_usuario(self):
        #pega a url de criar usuario
        url = reverse("list_create_usuario")

        usuario = {
            "username": "usuarioTeste",
            "password": "aaa",
            "cidade": self.cidade.id
        }

        RESPOSTA_ESPERADA = {'id': 5, 'user': 6, 'criador': 1, 'cidade': 1, 'ativo': True}

        response = self.client.post(url, usuario, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_criar_usuario_negado(self):
        #pega a url de criar usuario
        url = reverse("list_create_usuario")

        usuario = {
            "username": "",
            "password": "aaa",
            "cidade": self.cidade.id
        }

        RESPOSTA_ESPERADA = {'error': 'valor do username ou password não informado ou incorreto'}

        response = self.client.post(url, usuario, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    ### PUT
    def test_alterar_completamente_usuario(self):
        USUARIO_ID = 1
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        novaCidade = Cidade.objects.create(nome="cidadeTeste2", numero_habitantes=10)

        usuario = {
            "password": "senhaTeste",
            "cidade": novaCidade.id
        }

        RESPOSTA_ESPERADA = {'id': 1, 'user': 2, 'criador': 1, 'cidade': 2, 'ativo': True}

        response = self.client.put(url, usuario, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_alterar_completamente_usuario_negado(self):
        USUARIO_ID = 2
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        novaCidade = Cidade.objects.create(nome="cidadeTeste2", numero_habitantes=10)

        usuario = {
            "cidade": novaCidade.id
        }

        RESPOSTA_ESPERADA = {'error': 'passe todos e somente os campos obrigatórios'}

        response = self.client.put(url, usuario, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    #### PATCH
    def test_alterar_parcialmente_usuario(self):
        USUARIO_ID = 3
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        novaCidade = Cidade.objects.create(nome="cidadeTeste3", numero_habitantes=10)

        usuario = {
            "cidade": novaCidade.id
        }

        RESPOSTA_ESPERADA = {'id': 3, 'user': 4, 'criador': 1, 'cidade': 2, 'ativo': True}

        response = self.client.patch(url, usuario, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_alterar_parcialmente_usuario_negado(self):
        USUARIO_ID = 20
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        novaCidade = Cidade.objects.create(nome="cidadeTeste3", numero_habitantes=10)

        usuario = {
            "cidade": novaCidade.id
        }

        RESPOSTA_ESPERADA = {'error': 'usuário com id 20 não encontrado'}

        response = self.client.patch(url, usuario, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    ### DELETE
    def test_delete_usuario(self):
        USUARIO_ID = 4
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_delete_usuario_negado(self):
        USUARIO_ID = 20
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        RESPOSTA_ESPERADA = {'error': 'usuário com id 20 não encontrado'}

        response = self.client.delete(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CasoTeste(APITestCase):
    def setUp(self):
        user = User.objects.create(username='teste', password='teste', is_staff=True)
        self.client.force_authenticate(user=user)

        self.caso1 = Caso.objects.create(boletim=1, tipo='suspeito', genero='masculino', faixa='0-19', quantidade=10)
        self.caso2 = Caso.objects.create(boletim=2, tipo='notificado', genero='feminino', faixa='80+', quantidade=100)


    ### GET
    def test_listar_casos(self):
        url = reverse("list_create_caso")

        RESPOSTA_ESPERADA = 2

        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_listar_um_caso(self):
        CASO_ID = 1
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        RESPOSTA_ESPERADA = {
            'id': 1,
            'boletim': 1,
            'tipo': 'suspeito',
            'genero': 'masculino',
            'faixa': '0-19',
            'quantidade': 10,
            'ativo': True
        }

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_listar_um_caso_negado(self):
        CASO_ID = 10
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        RESPOSTA_ESPERADA = {'error': 'caso com id 10 não encontrado'}

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    ### POST
    def test_criar_um_caso(self):
        url = reverse("list_create_caso")

        caso = {
            'boletim': 2,
            'tipo': 'confirmado',
            'genero': 'outro',
            'faixa': '20-39',
            'quantidade': 10,
        }

        RESPOSTA_ESPERADA = {
            'id': 3,
            'boletim': 2,
            'tipo': 'confirmado',
            'genero': 'outro',
            'faixa': '20-39',
            'quantidade': 10,
            'ativo': True
        }

        response = self.client.post(url, caso, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_criar_um_caso_negado(self):
        url = reverse("list_create_caso")

        caso = {
            'boletim': 2,
            'tipo': 'aaa',
            'genero': 'outro',
            'faixa': '20-39',
            'quantidade': 10,
        }

        response = self.client.post(url, caso, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    ### PUT
    def test_alterar_completamente_caso(self):
        CASO_ID = 1
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        NOVOS_DADOS = {
            'boletim': 10,
            'tipo': 'obito',
            'genero': 'outro',
            'faixa': '40-59',
            'quantidade': 50,
        }
        
        RESPOSTA_ESPERADA = {
            'id': 1,
            'boletim': 10,
            'tipo': 'obito',
            'genero': 'outro',
            'faixa': '40-59',
            'quantidade': 50,
            'ativo': True
        }

        response = self.client.put(url, NOVOS_DADOS, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_alterar_completamente_caso_negado(self):
        CASO_ID = 1
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        NOVOS_DADOS_ERRADOS = {
            'boletim': 10,
            'tipo': 'obito',
            'genero': 'outro',
            'faixa': '40-59',
        }

        response = self.client.put(url, NOVOS_DADOS_ERRADOS, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    ### PATCH
    def test_alterar_parcialmente_caso(self):
        CASO_ID = 2
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        NOVOS_DADOS = {
            'boletim': 20,
        }
        
        RESPOSTA_ESPERADA = {
            'id': 2,
            'boletim': 20,
            'tipo': 'notificado',
            'genero': 'feminino',
            'faixa': '80+',
            'quantidade': 100,
            'ativo': True
        }

        response = self.client.patch(url, NOVOS_DADOS, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_alterar_parcialmente_caso_negado(self):
        CASO_ID = 2
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        NOVOS_DADOS_ERRADOS = {
            'faixa': '12-20',
        }

        response = self.client.put(url, NOVOS_DADOS_ERRADOS, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    ### DELETE
    def test_deletar_caso(self):
        CASO_ID = 2
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_deletar_caso_negado(self):
        CASO_ID = 20
        url = reverse("read_update_delete_caso", args=[CASO_ID])

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

