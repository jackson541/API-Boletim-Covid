from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
'''
    Na rota token, é preciso passar o parametro "username" e "password". Se os 
    dados estiverem corretos, irá retornar um campo "token". 
    Esse token deve ser utilizado nas requisições de administradores em determinadas
    rotas, pelo header, para validação de autenticação.

    Ex: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
'''
schema_view = get_schema_view(
    openapi.Info(
        title='API Covid-19',
        default_version='v1.0'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', views.obtain_auth_token),
    path('api/', include('apicovid.urls'), name='api'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
