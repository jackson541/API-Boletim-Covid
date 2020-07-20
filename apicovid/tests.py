from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Cidade, Usuario, Boletim

'''
    OBS: o Django cria um db separado para os testes
'''

class UsuarioTeste(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='teste', password='teste', is_staff=True)
        self.cidade = Cidade.objects.create(nome='cidadeTeste', numero_habitantes=10)

        # cidades para teste
        self.cidade1 = Cidade.objects.create(nome="Jucurutu", numero_habitantes=20000)
        self.cidade2 = Cidade.objects.create(nome="Caicó", numero_habitantes=70000)
        self.cidade3 = Cidade.objects.create(nome="São João do Sabugi", numero_habitantes=6200)

        #força autenticação para não precisa do token
        self.client.force_authenticate(user=self.user)

        ## usuários padrões para teste
        user1 = User.objects.create(username='testeListagem1', password='teste')
        user2 = User.objects.create(username='testeListagem2', password='teste')
        user3 = User.objects.create(username='testeListagem3', password='teste')
        user4 = User.objects.create(username='testeListagem4', password='teste')

        self.usuario1 = Usuario.objects.create(user=user1, criador=self.user, cidade=self.cidade)
        self.usuario2 = Usuario.objects.create(user=user2, criador=self.user, cidade=self.cidade)
        self.usuario3 = Usuario.objects.create(user=user3, criador=self.user, cidade=self.cidade)
        self.usuario4 = Usuario.objects.create(user=user4, criador=self.user, cidade=self.cidade)

    def test_listar_cidades(self):
        url = reverse("list_create_cidade")

        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_cidade3(self):
        CIDADE_ID = self.cidade3.id
        url = reverse("read_update_delete_cidade", args=[CIDADE_ID])

        RESPOSTA_ESPERADA = {
            'id': self.cidade3.id,   
            'nome': "São João do Sabugi", 
            'numero_habitantes': 6200,
            'ativo': True
        }

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listar_cidade1(self):
        CIDADE_ID = self.cidade1.id
        url = reverse("read_update_delete_cidade", args=[CIDADE_ID])

        RESPOSTA_ESPERADA = {
            'id': self.cidade1.id,   
            'nome': "Jucurutu", 
            'numero_habitantes': 20000,
            'ativo': True
        }

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    ### GET
    def test_listar_usuarios(self):
        url = reverse("list_create_usuario")

        NUM_CASOS_LISTADOS = 4

        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), NUM_CASOS_LISTADOS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_listar_um_usuario(self):
        USUARIO_ID = self.usuario2.id
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        RESPOSTA_ESPERADA = {'id': self.usuario2.id, 
                             'user': self.usuario2.user.id, 
                             'criador': self.usuario2.criador.id, 
                             'cidade': self.usuario2.cidade.id, 
                             'ativo': True, 
                             'username': 'testeListagem2'}

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

        RESPOSTA_ESPERADA = {'id': (self.usuario4.id + 1), 
                             'user': (self.usuario4.user.id + 1), 
                             'criador': self.usuario4.criador.id, 
                             'cidade': self.usuario4.cidade.id, 
                             'ativo': True, 
                             "username": "usuarioTeste"}

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
        USUARIO_ID = self.usuario1.id
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        novaCidade = Cidade.objects.create(nome="cidadeTeste2", numero_habitantes=10)

        usuario = {
            "password": "senhaTeste",
            "cidade": novaCidade.id
        }

        RESPOSTA_ESPERADA = {'id': self.usuario1.id,
                             'user': self.usuario1.user.id, 
                             'criador': self.usuario1.criador.id, 
                             'cidade': novaCidade.id,
                             'ativo': True, 
                             "username": "testeListagem1"}

        response = self.client.put(url, usuario, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_alterar_completamente_usuario_negado(self):
        USUARIO_ID = self.usuario2.id
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
        USUARIO_ID = self.usuario3.id
        url = reverse("read_update_delete_usuario", args=[USUARIO_ID])

        novaCidade = Cidade.objects.create(nome="cidadeTeste3", numero_habitantes=10)

        usuario = {
            "cidade": novaCidade.id
        }

        RESPOSTA_ESPERADA = {'id': self.usuario3.id, 'user': self.usuario3.user.id, 'criador': self.usuario3.criador.id, 'cidade': novaCidade.id, 'ativo': True, 'username': 'testeListagem3'}

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
        USUARIO_ID = self.usuario4.id
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


class BoletimTeste(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='teste', password='teste', is_staff=True)
        self.cidade = Cidade.objects.create(nome="cidadeTeste", numero_habitantes=10)

        Usuario.objects.create(user=self.user, criador=self.user, cidade=self.cidade)

        #força autenticação para não precisa do token
        self.client.force_authenticate(user=self.user)

        ## boletins padrões para teste
        self.boletim1 = Boletim.objects.create(cidade = self.cidade,
                                                data = '2020-10-25 00:00:00',
                                                casosConfirmados = 10,
                                                casosEmTratamento = 10,
                                                casosInternados = 10,
                                                casosRecuperados = 10,
                                                casosSuspeitos = 10,
                                                casosDeObito = 10,
                                                casosDescartados = 10,
                                                casosNotificados = 10)

        self.boletim2 = Boletim.objects.create(cidade = self.cidade,
                                                data = '2020-10-25 00:00:00',
                                                casosConfirmados = 10,
                                                casosEmTratamento = 10,
                                                casosInternados = 10,
                                                casosRecuperados = 10,
                                                casosSuspeitos = 10,
                                                casosDeObito = 10,
                                                casosDescartados = 10,
                                                casosNotificados = 10)
        
    ### GET
    def test_listar_boletins(self):
        url = reverse("list_create_boletim")

        NUM_BOLETINS_LISTADOS = 2

        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), NUM_BOLETINS_LISTADOS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_listar_um_boletim(self):
        BOLETIM_ID = self.boletim2.id
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        RESPOSTA_ESPERADA = {'id': self.boletim2.id, 
                             'cidade': self.boletim2.cidade.id,
                             'data': '2020-10-25T00:00:00Z',
                             'casosConfirmados': 10,
                             'casosEmTratamento': 10,
                             'casosInternados': 10,
                             'casosRecuperados': 10,
                             'casosSuspeitos': 10,
                             'casosDeObito': 10,
                             'casosDescartados': 10,
                             'casosNotificados': 10,
                             'ativo': True}

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_listar_um_boletim_negado(self):
        BOLETIM_ID = 20
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        RESPOSTA_ESPERADA = {'error': 'boletim com id 20 não encontrado'}

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    ### POST
    def test_criar_boletim(self):
        url = reverse("list_create_boletim")

        boletim = {
            'cidade': self.cidade.id,
            'data': '2020-10-26T00:00:00Z',
            'casosConfirmados': 1,
            'casosEmTratamento': 1,
            'casosInternados': 1,
            'casosRecuperados': 1,
            'casosSuspeitos': 1,
            'casosDeObito': 1,
            'casosDescartados': 1,
            'casosNotificados': 1,
        }

        RESPOSTA_ESPERADA = {'id': (self.boletim2.id + 1), 
                             'cidade': self.cidade.id,
                             'data': '2020-10-26T00:00:00Z',
                             'casosConfirmados': 1,
                             'casosEmTratamento': 1,
                             'casosInternados': 1,
                             'casosRecuperados': 1,
                             'casosSuspeitos': 1,
                             'casosDeObito': 1,
                             'casosDescartados': 1,
                             'casosNotificados': 1,
                             'ativo': True}

        response = self.client.post(url, boletim, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_criar_boletim_negado(self):
        url = reverse("list_create_boletim")

        boletim = {
            'cidade': self.cidade.id,
            'data': '',
            'casosConfirmados': 1,
            'casosEmTratamento': 1,
            'casosInternados': 1,
            'casosRecuperados': 1,
            'casosSuspeitos': 1,
            'casosDeObito': 1,
            'casosDescartados': 1,
            'casosNotificados': 1,
        }

        response = self.client.post(url, boletim, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    ### PUT
    def test_alterar_completamente_boletim(self):
        BOLETIM_ID = self.boletim2.id
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        boletim = {
            'data': '2021-10-26T00:00:00Z',
            'casosConfirmados': 15,
            'casosEmTratamento': 15,
            'casosInternados': 15,
            'casosRecuperados': 15,
            'casosSuspeitos': 15,
            'casosDeObito': 15,
            'casosDescartados': 15,
            'casosNotificados': 15,
        }

        RESPOSTA_ESPERADA = {
            'id': self.boletim2.id,
            'data': '2021-10-26T00:00:00Z',
            'ativo': True,
            'casosConfirmados': 15,
            'casosEmTratamento': 15,
            'casosInternados': 15,
            'casosRecuperados': 15,
            'casosSuspeitos': 15,
            'casosDeObito': 15,
            'casosDescartados': 15,
            'casosNotificados': 15,
            'cidade': self.cidade.id
        }

        response = self.client.put(url, boletim, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_alterar_completamente_boletim_negado(self):
        BOLETIM_ID = self.boletim2.id
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        novaCidade = Cidade.objects.create(nome="cidadeTeste2", numero_habitantes=10)

        boletim = {
            'cidade': novaCidade.id,
            'data': '2021-10-26T00:00:00Z',
            'casosConfirmados': 15,
            'casosEmTratamento': 15,
            'casosInternados': 15,
            'casosRecuperados': -15,
            'casosSuspeitos': 15,
            'casosDeObito': 15,
            'casosDescartados': 15,
            'casosNotificados': 15,
        }

        response = self.client.put(url, boletim, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    #### PATCH
    def test_alterar_parcialmente_boletim(self):
        BOLETIM_ID = self.boletim2.id
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        boletim = {
            'casosRecuperados': 100,
        }

        RESPOSTA_ESPERADA = {
            'id': self.boletim2.id,
            'data': '2020-10-25T00:00:00Z',
            'ativo': True,
            'casosConfirmados': 10,
            'casosEmTratamento': 10,
            'casosInternados': 10,
            'casosRecuperados': 100,
            'casosSuspeitos': 10,
            'casosDeObito': 10,
            'casosDescartados': 10,
            'casosNotificados': 10,
            'cidade': self.boletim2.cidade.id
        }

        response = self.client.patch(url, boletim, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_alterar_parcialmente_boletim_negado(self):
        BOLETIM_ID = 20
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        boletim = {
            'casosRecuperados': 100,
        }

        RESPOSTA_ESPERADA = {'error': 'boletim com id 20 não encontrado'}

        response = self.client.patch(url, boletim, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    ### DELETE
    def test_delete_boletim(self):
        BOLETIM_ID = self.boletim1.id
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_delete_boletim_negado(self):
        BOLETIM_ID = 20
        url = reverse("read_update_delete_boletim", args=[BOLETIM_ID])

        RESPOSTA_ESPERADA = {'error': 'boletim com id 20 não encontrado'}

        response = self.client.delete(url, format='json')
        self.assertEqual(response.data, RESPOSTA_ESPERADA)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)