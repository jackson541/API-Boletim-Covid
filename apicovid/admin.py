from django.contrib import admin
from .models import *

def deletarCidade(modeladmin, request, queryset):
    for cidade in queryset.values():
        usuarios = Usuario.objects.filter(cidade=cidade['id'])
        usuarios.update(ativo=False)
        
    queryset.update(ativo=False)


def restaurarCidade(modeladmin, request, queryset):
    for cidade in queryset.values():
        usuarios = Usuario.objects.filter(cidade=cidade['id'])
        usuarios.update(ativo=True)
        
    queryset.update(ativo=True)
    

deletarCidade.short_description = "Marcar como inativa"
restaurarCidade.short_description = "Marcar como ativa"

class CidadeAdmin(admin.ModelAdmin):
    actions=[deletarCidade, restaurarCidade]

admin.site.register(Usuario)
admin.site.register(Cidade, CidadeAdmin)
