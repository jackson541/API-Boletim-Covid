from django.contrib import admin
from .models import *

def deletarCidade(modeladmin, request, queryset):
    listaIdsCidades = queryset.values_list('id', flat=True)
    queryset.update(ativo=False)

    usuarios = Usuario.objects.filter(cidade__in=listaIdsCidades)
    usuarios.update(ativo=False)

    boletins = Boletim.objects.filter(cidade__in=listaIdsCidades)
    boletins.update(ativo=False)

    listaIdsBoletins = boletins.values_list('id', flat=True)
    
    casosRelacionados = Caso.objects.filter(boletim__in=listaIdsBoletins)
    casosRelacionados.update(ativo=False)


def restaurarCidade(modeladmin, request, queryset):
    listaIdsCidades = queryset.values_list('id', flat=True)
    queryset.update(ativo=True)

    usuarios = Usuario.objects.filter(cidade__in=listaIdsCidades)
    usuarios.update(ativo=True)

    boletins = Boletim.objects.filter(cidade__in=listaIdsCidades)
    boletins.update(ativo=True)

    listaIdsBoletins = boletins.values_list('id', flat=True)
    
    casosRelacionados = Caso.objects.filter(boletim__in=listaIdsBoletins)
    casosRelacionados.update(ativo=True)
    

deletarCidade.short_description = "Marcar como inativa"
restaurarCidade.short_description = "Marcar como ativa"

class CidadeAdmin(admin.ModelAdmin):
    actions=[deletarCidade, restaurarCidade]

admin.site.register(Usuario)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Boletim)
admin.site.register(Caso)
