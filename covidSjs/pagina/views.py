from django.shortcuts import render
from django.views import View
import datetime

from .models import casos as Casos

# Create your views here.

def gerarDadosGraficos(casoAtual):
    primeiroCaso = Casos.objects.first()
    diferencaEmDias = (casoAtual.data - primeiroCaso.data).days + 1
    saltoEntreDatas = diferencaEmDias/10
    
    datas = []

    #adiciona todas as datas que obedecem ao intervalo de saltos
    for x in range(10):
        datas.append(
            primeiroCaso.data + datetime.timedelta(saltoEntreDatas * x)
        )

    datas.append(casoAtual.data)

    '''
        Pega os números de 'confirmados' dos objetos que estão com as datas
        cadastrada em 'datas' e salva na lista 'graficoCasosConfirmados'. Se o 
        objeto com a data passada não existir, ele irá pegar o último objeto 
        listado (por meio da lista gerada pelo '__lte') mais próximo.
    '''
    graficoCasosConfirmados = [Casos.objects.filter(data__lte=data).latest().confirmados
                                    for data in datas
    ]

    graficoCasosRecuperados = [Casos.objects.filter(data__lte=data).latest().recuperados
                                    for data in datas
    ]
    
    graficoCasosSuspeitos = [Casos.objects.filter(data__lte=data).latest().suspeitos
                                    for data in datas
    ]

    graficoCasosDescartados = [Casos.objects.filter(data__lte=data).latest().descartados
                                    for data in datas
    ]

    graficoCasosObitos = [Casos.objects.filter(data__lte=data).latest().obitos
                                    for data in datas
    ]
    
    #converte as datas para string no formato dia/mes
    datas = [data.strftime('%d/%m') for data in datas]

    return datas, graficoCasosConfirmados, graficoCasosRecuperados, graficoCasosSuspeitos, graficoCasosDescartados, graficoCasosObitos


class index(View):
    def get(self, request):
        casoAtual = Casos.objects.latest('data')

        datas, graficoCasosConfirmados, graficoCasosRecuperados, graficoCasosSuspeitos, graficoCasosDescartados, graficoCasosObitos = gerarDadosGraficos(casoAtual)

        # inverte a ordem da lista completa de objetos, que estão ordenados pela
        # data, e pega o segundo da lista (penúltimo)
        penultimoCaso = Casos.objects.order_by('data')[::-1][1]

        casosNovos = {
            'confirmados': casoAtual.confirmados - penultimoCaso.confirmados,
            'recuperados': casoAtual.recuperados - penultimoCaso.recuperados,
            'suspeitos': casoAtual.suspeitos - penultimoCaso.suspeitos,
            'descartados': casoAtual.descartados - penultimoCaso.descartados,
            'obitos': casoAtual.obitos - penultimoCaso.obitos
        }

        return render(request, 'index.html', {'casoAtual': casoAtual, 
                                            'casosNovos': casosNovos,
                                            'datas': datas,
                            'graficoCasosConfirmados': graficoCasosConfirmados,
                            'graficoCasosRecuperados': graficoCasosRecuperados,
                            'graficoCasosSuspeitos': graficoCasosSuspeitos,
                            'graficoCasosDescartados': graficoCasosDescartados,
                            'graficoCasosObitos': graficoCasosObitos,
        })
