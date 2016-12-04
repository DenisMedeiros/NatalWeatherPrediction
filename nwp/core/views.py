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
        #corrigir_dados_tratados()
        #popular_db()
        criar_conjunto_treinamento()

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
    arquivo_escrita = open(
        os.path.join(diretorio, 'resource', 'dados_tratados.csv'), 'wb')

    reader = csv.reader(arquivo_leitura, delimiter=';')
    writer = csv.writer(arquivo_escrita, delimiter=';')

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
        arquivo_escrita.close()

def popular_db():
    diretorio = os.path.dirname(__file__)
    arquivo_leitura = open(
        os.path.join(diretorio, 'resource', 'dados_tratados_corrigidos.csv'), 'rb')

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
            data = datetime.datetime.strptime(data, '%d/%m/%Y')

            try:   
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
                print data
                pass

    except StopIteration:
        print 'Dados inseridos no banco de dados.'
        arquivo_leitura.close()


def corrigir_dados_tratados():
    diretorio = os.path.dirname(__file__)
    arquivo_leitura = open(
        os.path.join(diretorio, 'resource', 'dados_tratados.csv'), 'rb')
    arquivo_escrita = open(
        os.path.join(diretorio, 'resource', 'dados_tratados_corrigidos.csv'), 'wb')

    reader = csv.reader(arquivo_leitura, delimiter=';')
    writer = csv.writer(arquivo_escrita, delimiter=';')

    # Ignora a primeira linha
    reader.next()

    writer.writerow(['data', 'temperatura_min', 'temperatura_max',
        'temperatura_media', 'humidade_media', 'insolacao',
        'velocidade_vento', 'precipitacao'])


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
            data = datetime.datetime.strptime(data, '%d/%m/%Y')

            if not temperatura_min:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if Amostra.objects.filter(data=anterior).exists():
                        temperatura_min = Amostra.objects.get(data=anterior).temperatura_min
                        break

            if not temperatura_max:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if Amostra.objects.filter(data=anterior).exists():
                        temperatura_max = Amostra.objects.get(data=anterior).temperatura_max
                        break

            if not temperatura_media:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if Amostra.objects.filter(data=anterior).exists():
                        temperatura_media = Amostra.objects.get(data=anterior).temperatura_media
                        break

            if not humidade_media:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if Amostra.objects.filter(data=anterior).exists():
                        humidade_media = Amostra.objects.get(data=anterior).humidade_media
                        break

            if not insolacao:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if Amostra.objects.filter(data=anterior).exists():
                        insolacao = Amostra.objects.get(data=anterior).insolacao
                        break

            if not velocidade_vento:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if Amostra.objects.filter(data=anterior).exists():
                        velocidade_vento = Amostra.objects.get(data=anterior).velocidade_vento
                        break

            if not precipitacao:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if Amostra.objects.filter(data=anterior).exists():
                        precipitacao = Amostra.objects.get(data=anterior).precipitacao
                        break


            try:   
                temperatura_min = float(temperatura_min)
                temperatura_max = float(temperatura_max)
                temperatura_media = float(temperatura_media)
                humidade_media = float(humidade_media)
                insolacao = float(insolacao)
                velocidade_vento = float(velocidade_vento)
                precipitacao = float(precipitacao)

                writer.writerow([data.strftime('%d/%m/%Y'), temperatura_min, temperatura_max,
                    temperatura_media, humidade_media, insolacao,
                    velocidade_vento, precipitacao])

            except Exception, e:
                print 'Erro na data ', data
                print e


    except StopIteration:
        print 'Dados corrigidos.'
        arquivo_leitura.close()
        arquivo_leitura.close()


def criar_conjunto_treinamento():
    diretorio = os.path.dirname(__file__)
    todas_amostras = Amostra.objects.all()
    quantidade = len(todas_amostras)
    indices_amostras = random.sample(xrange(2, quantidade, 1), 2000)

    arquivo_escrita = open(
        os.path.join(diretorio, 'resource', 'conjunto_treinamento.csv'), 'wb')

    writer = csv.writer(arquivo_escrita, delimiter=';')

    writer.writerow([
        'mes', 'temperatura_min1', 'temperatura_min2',
        'temperatura_max1', 'temperatura_max2', 'humidade_media1',
        'humidade_media2', 'insolacao1', 'insolacao2', 'velocidade_vento1',
        'velocidade_vento2', 'precipitacao', 'temperatura_min', 
        'temperatura_max', 'humidade_media',
    ])

    for i in indices_amostras:

        amostra0 = todas_amostras[i]
        amostra1 = todas_amostras[i-1]
        amostra2 = todas_amostras[i-2]

        # Dados da entrada.

        mes = amostra0.data.month

        temperatura_min1 = amostra1.temperatura_min
        temperatura_min2 = amostra2.temperatura_min

        temperatura_max1 = amostra1.temperatura_max
        temperatura_max2 = amostra2.temperatura_max

        humidade_media1 = amostra1.humidade_media
        humidade_media2 = amostra2.humidade_media

        insolacao1 = amostra1.insolacao
        insolacao2 = amostra2.insolacao

        velocidade_vento1 = amostra1.velocidade_vento
        velocidade_vento2 = amostra2.velocidade_vento

        # Dados da saída.

        precipitacao = amostra0.precipitacao
        temperatura_min = amostra0.temperatura_min
        temperatura_max = amostra0.temperatura_max
        humidade_media = amostra0.humidade_media

        writer.writerow([
        mes, temperatura_min1, temperatura_min2,
        temperatura_max1, temperatura_max2, humidade_media1,
        humidade_media2, insolacao1, insolacao2, velocidade_vento1,
        velocidade_vento2, precipitacao, temperatura_min, 
        temperatura_max, humidade_media,
        ])


    arquivo_escrita.close()
    print "Conjunto treinamento criado com sucesso!"
    