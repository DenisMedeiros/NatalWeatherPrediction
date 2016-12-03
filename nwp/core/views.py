# -*- coding: utf-8 -*-

import os, csv, datetime, random
from django.shortcuts import render
from django.views.generic import View
from .models import Amostra

# Create your views here.

class PaginaInicialView(View):

    def get(self, request):

        # Descomente a linha abaixo para preencher o banco de dados.
        #tratar_dados()
        #popular_db()
        realizar_treinamento()

        context = {
            'hoje': datetime.datetime.now(),
        }
        return render(request, 'pagina_inicial.html', context)

class SobreView(View):

    def get(self, request):
        context = {
        }
        return render(request, 'sobre.html', context)



######## As função abaixo são puramente auxilares. ##########


# Trata os dados fornecidos pelo INMEP.
def tratar_dados():
    diretorio = os.path.dirname(__file__)
    arquivo_leitura = open(
        os.path.join(diretorio, 'resource', 'dados_inmet.csv'), 'rb')
    arquivo_saida = open(
        os.path.join(diretorio, 'resource', 'dados_tratados.csv'), 'wb')

    reader = csv.reader(arquivo_leitura, delimiter=';')
    writer = csv.writer(arquivo_saida, delimiter=';')

    writer.writerow(['data', 'temperatura_min', 'temperatura_max',
        'temperatura_media', 'humidade_media', 'insolacao',
        'velocidade_vento', 'precipitacao'])

    try:
        while True:
            coleta_00 = reader.next()
            coleta_12 = reader.next()

            estacao = coleta_00[0]
            data = coleta_00[1]
            hora = coleta_00[2]

            if coleta_12[3]:
                precipitacao = coleta_12[3]
            else:
                precipitacao = coleta_00[3]

            if coleta_00[4]:
                temperatura_max = coleta_00[4]
            else:
                temperatura_max = coleta_12[4]

            if coleta_12[5]:
                temperatura_min = coleta_12[5]
            else:
                temperatura_min = coleta_00[5]

            if coleta_00[6]:
                insolacao = coleta_00[6]
            else:
                insolacao = coleta_12[6]

            if coleta_00[7]:
                temperatura_media = coleta_00[7]
            else:
                temperatura_media = coleta_12[7]

            if coleta_00[8]:
                humidade_media = coleta_00[8]
            else:
                humidade_media = coleta_12[8]

            if coleta_00[9]:
                velocidade_vento = coleta_00[9]
            else:
                velocidade_vento = coleta_12[9]

            writer.writerow([data, temperatura_min, temperatura_max,
            temperatura_media, humidade_media, insolacao, velocidade_vento,
            precipitacao])

    except StopIteration:
        print 'Tratamento dos dados encerrado'
        arquivo_leitura.close()
        arquivo_saida.close()

def popular_db():
    diretorio = os.path.dirname(__file__)
    arquivo_leitura = open(
        os.path.join(diretorio, 'resource', 'dados_tratados.csv'), 'rb')

    reader = csv.reader(arquivo_leitura, delimiter=';')

    # Remove os cabeçalhos.
    reader.next()
    i = 0
    try:
        while True:

            coleta = reader.next()

            data = coleta[0]
            temperatura_min = coleta[1]
            temperatura_max = coleta[2]
            temperatura_media = coleta[3]
            humidade_media = coleta[4]
            insolacao = coleta[5]
            velocidade_vento = coleta[6]
            precipitacao = coleta[7]

            # Prepara os dados para criar o objeto.
            try:
                data = datetime.datetime.strptime(data, '%d/%m/%Y')
                temperatura_min = float(temperatura_min)
                temperatura_max = float(temperatura_max)
                temperatura_media = float(temperatura_media)
                humidade_media = float(humidade_media)
                insolacao = float(insolacao)
                velocidade_vento = float(velocidade_vento)
                precipitacao = float(precipitacao)

                if(not Amostra.objects.filter(data=data).exists()):
                    print data
                    amostra = Amostra(
                        data = data,
                        temperatura_min = temperatura_min,
                        temperatura_max = temperatura_max,
                        temperatura_media = temperatura_media,
                        humidade_media = humidade_media,
                        insolacao = insolacao,
                        velocidade_vento = velocidade_vento,
                        precipitacao = precipitacao,
                    )

                    amostra.save()

            except Exception, e:
                pass

    except StopIteration:
        print 'Dados inseridos no banco de dados.'
        arquivo_leitura.close()


def realizar_treinamento():
    todas_amostras = Amostra.objects.all()
    amostras_treinamento = random.sample(todas_amostras, 3000)

    #
