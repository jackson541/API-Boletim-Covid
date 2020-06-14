from django.shortcuts import render
from django.views import View
import datetime

from .models import casos as Casos

# Create your views here.

def gerarDadosGraficos(casoAtual):
    primeiroCaso = Casos.objects.first()
    diferencaEmDias = (casoAtual.data - primeiroCaso.data).days + 1

    # O salto serve para pegar 11 datas com espaçamento igual entre a primeira e
    # a última data cadastrada.
    saltoEntreDatas = diferencaEmDias/10
    
    datas = []

    #adiciona todas as datas que obedecem ao intervalo de saltos
    for x in range(10):
        datas.append(
            primeiroCaso.data + datetime.timedelta(saltoEntreDatas * x)
        )

    datas.append(casoAtual.data)

    graficoCasosConfirmados = []
    graficoCasosConfirmadosTotal = []
    graficoCasosRecuperados = []
    graficoCasosSuspeitos = []
    graficoCasosDescartados = []
    graficoCasosObitos = []

    '''
        Pega os números dos objetos que estão com as datas cadastrada em 'datas'
        e salva nas respectivas listas. Se o objeto com a data passada não 
        existir, ele irá pegar o último objeto listado (por meio da lista gerada
        pelo '__lte') mais próximo.
    '''
    for data in datas:
        casoParaAdicionar = Casos.objects.filter(data__lte=data).latest()

        graficoCasosConfirmados.append(casoParaAdicionar.confirmados)
        graficoCasosConfirmadosTotal.append(casoParaAdicionar.confirmados + casoParaAdicionar.recuperados)
        graficoCasosRecuperados.append(casoParaAdicionar.recuperados)
        graficoCasosSuspeitos.append(casoParaAdicionar.suspeitos)
        graficoCasosDescartados.append(casoParaAdicionar.descartados)
        graficoCasosObitos.append(casoParaAdicionar.obitos)

    
    #converte as datas para string no formato dia/mes
    datas = [data.strftime('%d/%m') for data in datas]

    return datas, graficoCasosConfirmados, graficoCasosConfirmadosTotal, graficoCasosRecuperados, graficoCasosSuspeitos, graficoCasosDescartados, graficoCasosObitos


class index(View):
    def get(self, request):
        casoAtual = Casos.objects.latest('data')

        #adicionar os casos atuais que não existem na modelagem do banco de dados
        casoAtual.confirmadosTotal = casoAtual.confirmados + casoAtual.recuperados

        datas, graficoCasosConfirmados, graficoCasosConfirmadosTotal, graficoCasosRecuperados, graficoCasosSuspeitos, graficoCasosDescartados, graficoCasosObitos = gerarDadosGraficos(casoAtual)

        # inverte a ordem da lista completa de objetos, que estão ordenados pela
        # data, e pega o segundo da lista (penúltimo)
        penultimoCaso = Casos.objects.order_by('data')[::-1][1]

        '''
            Se o diferença dos casos novos for maior ou igual a 0, permanecerá o
             valor, se não, o valor passado será 0
        '''
        casosNovos = {
            'confirmados': casoAtual.confirmados - penultimoCaso.confirmados if casoAtual.confirmados - penultimoCaso.confirmados >=0 else 0,
            'confirmadosTotal': casoAtual.confirmadosTotal - (penultimoCaso.confirmados + penultimoCaso.recuperados), 
            'recuperados': casoAtual.recuperados - penultimoCaso.recuperados,
            'suspeitos': casoAtual.suspeitos - penultimoCaso.suspeitos if casoAtual.suspeitos - penultimoCaso.suspeitos >=0 else 0,
            'descartados': casoAtual.descartados - penultimoCaso.descartados,
            'obitos': casoAtual.obitos - penultimoCaso.obitos
        }

        return render(request, 'index.html', {'casoAtual': casoAtual, 
                                            'casosNovos': casosNovos,
                                            'datas': datas,
                    'graficoCasosConfirmados': graficoCasosConfirmados,
                    'graficoCasosConfirmadosTotal': graficoCasosConfirmadosTotal,
                    'graficoCasosRecuperados': graficoCasosRecuperados,
                    'graficoCasosSuspeitos': graficoCasosSuspeitos,
                    'graficoCasosDescartados': graficoCasosDescartados,
                    'graficoCasosObitos': graficoCasosObitos,
        })
