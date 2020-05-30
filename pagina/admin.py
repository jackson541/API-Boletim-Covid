from django.contrib import admin
from .models import casos

# Register your models here.

### correção de erro
'''
    Ocorreu um erro ao tentar apagar uma data com a ação padrão em massa do
    django. o código a seguir corrige esse problema removendo essa função e 
    colocando uma semelhante no lugar.
'''
def delete_casos(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()
delete_casos.short_description = "Remover casos selecionados"

class deletarCasos(admin.ModelAdmin):
    actions = [delete_casos]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(casos, deletarCasos)