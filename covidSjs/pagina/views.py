from django.shortcuts import render
from django.views import View

from .models import casos as Casos

# Create your views here.

class index(View):
    def get(self, request):
        casoAtual = Casos.objects.latest('data')

        # inverte a ordem da lista completa de objetos, que estão ordenados pela
        # data, e pega o segundo da lista (penúltimo)
        penultimoCaso = Casos.objects.all().order_by('data')[::-1][1]

        casosNovos = {
            'confirmados': casoAtual.confirmados - penultimoCaso.confirmados,
            'recuperados': casoAtual.recuperados - penultimoCaso.recuperados,
            'suspeitos': casoAtual.suspeitos - penultimoCaso.suspeitos,
            'descartados': casoAtual.descartados - penultimoCaso.descartados,
            'obitos': casoAtual.obitos - penultimoCaso.obitos
        }

        return render(request, 'index.html', {'casoAtual': casoAtual, 
                                            'casosNovos': casosNovos})
