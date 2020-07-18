from django.urls import path
from . import views

urlpatterns = [
    # URLs Cidade
    path('cidades/', views.CidadeList.as_view(), name='list_create_cidade'),
    path('cidades/<int:pk>/',
         views.CidadeDetail.as_view(),
         name='read_update_delete_cidade'),

    # URLs Usuario
    path('usuarios/', views.UsuarioList.as_view(), name='list_create_usuario'),
    path('usuarios/<int:pk>/',
         views.UsuarioDetail.as_view(),
         name='read_update_delete_usuario'),

    # URLs Boletim
    path('boletins/', views.BoletimList.as_view(), name='list_create_boletim'),
    path('boletins/<int:pk>/',
         views.BoletimDetail.as_view(),
         name='read_update_delete_boletim'),
]
