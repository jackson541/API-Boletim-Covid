from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views


'''
    Na rota token, é preciso passar o parametro "username" e "password". Se os 
    dados estiverem corretos, irá retornar um campo "token". 
    Esse token deve ser utilizado nas requisições de administradores em determinadas
    rotas, pelo header, para validação de autenticação.

    Ex: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', views.obtain_auth_token),
    path('api/', include('apicovid.urls'), name='api')
]
