from django.urls import path
from . import views

urlpatterns = [
    # URLs Cidade
    path('cidades/', views.CidadeList.as_view(), name='list_create_cidade'),
    path('cidades/<int:pk>/', views.CidadeDetail.as_view(), name='read_update_delete_cidade'),
    # URLs Caso
    path('casos/', views.CasoList.as_view(), name='list_create_caso'),
    path('casos/<int:pk>/', views.CasoDetail.as_view(), name='read_update_delete_caso'),
    #URLs Usuario
    path('usuarios/', views.UsuarioList.as_view(), name='list_create_usuario'),
    path('usuarios/<int:pk>/', views.UsuarioDetail.as_view(), name='read_update_delete_usuario'),
]