#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os, random, datetime

tamanho_treinamento = 5000
tamanho_validacao = 1000

def coletas_dict(nome_arquivo):
    diretorio = os.path.dirname(__file__)
    arquivo_leitura = open(
        os.path.join(diretorio, 'dados', nome_arquivo), 'rb')

    reader = csv.reader(arquivo_leitura, delimiter=';')
    # Ignora a primeira linha
    reader.next()

    # Lê o arquivo com os dados e armazena os não defeituosos em um dicionário.
    coletas = {}
    try:
        while True:
            coleta = reader.next()
            data = coleta[0]
            temperatura_min = coleta[1]
            temperatura_max = coleta[2]
            temperatura_media = coleta[3]
            umidade_media = coleta[4]
            insolacao = coleta[5]
            velocidade_vento = coleta[6]
            precipitacao = coleta[7]

            data = datetime.datetime.strptime(data, '%d/%m/%Y')

            try:
                temperatura_min = float(temperatura_min)
                temperatura_max = float(temperatura_max)
                temperatura_media = float(temperatura_media)
                umidade_media = float(umidade_media)
                insolacao = float(insolacao)
                velocidade_vento = float(velocidade_vento)
                precipitacao = float(precipitacao)

                coletas[data] = {
                    'temperatura_min': temperatura_min,
                    'temperatura_max': temperatura_max,
                    'temperatura_media': temperatura_media,
                    'umidade_media': umidade_media,
                    'insolacao': insolacao,
                    'velocidade_vento': velocidade_vento,
                    'precipitacao': precipitacao,
                }
            except ValueError as e:
                pass
    except StopIteration as e:
        pass

    return coletas


'''
Trata os dados fornecidos pelo INMEP., de modo a unificar as coletas em um
único dia.
'''
def tratar_dados():
    diretorio = os.path.dirname(__file__)
    arquivo_leitura = open(
        os.path.join(diretorio, 'dados', 'dados_inmet.csv'), 'rb')
    arquivo_escrita = open(
        os.path.join(diretorio, 'dados', 'dados_tratados.csv'), 'wb')

    reader = csv.reader(arquivo_leitura, delimiter=';')
    writer = csv.writer(arquivo_escrita, delimiter=';')

    writer.writerow(['data', 'temperatura_min', 'temperatura_max',
        'temperatura_media', 'umidade_media', 'insolacao',
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
                umidade_media = coleta_00[8]
            else:
                umidade_media = coleta_12[8]

            if coleta_00[9]:
                velocidade_vento = coleta_00[9]
            else:
                velocidade_vento = coleta_12[9]

            writer.writerow([data, temperatura_min, temperatura_max,
            temperatura_media, umidade_media, insolacao, velocidade_vento,
            precipitacao])

    except StopIteration:
        print '[1] Tratamento dos dados realizado com sucesso.'
        arquivo_leitura.close()
        arquivo_escrita.close()


'''
Corrige os campos em branco dos dados tratados anteriormente.
'''
def corrigir_dados_tratados():
    diretorio = os.path.dirname(__file__)
    arquivo_escrita = open(
        os.path.join(diretorio, 'dados', 'dados_tratados_corrigidos.csv'), 'wb')

    writer = csv.writer(arquivo_escrita, delimiter=';')
    # Escreve os cabeçalhos.
    writer.writerow(['data', 'temperatura_min', 'temperatura_max',
        'temperatura_media', 'umidade_media', 'insolacao',
        'velocidade_vento', 'precipitacao'])

    # Lê o arquivo com os dados e armazena os não defeituosos em um dicionário.
    coletas_corretas = coletas_dict('dados_tratados.csv')

    arquivo_leitura = open(
        os.path.join(diretorio, 'dados', 'dados_tratados.csv'), 'rb')
    # Armazena os dados.
    reader = csv.reader(arquivo_leitura, delimiter=';')
    # Ignora a primeira linha
    reader.next()

    try:
        while True:
            coleta = reader.next()
            data = coleta[0]
            temperatura_min = coleta[1]
            temperatura_max = coleta[2]
            temperatura_media = coleta[3]
            umidade_media = coleta[4]
            insolacao = coleta[5]
            velocidade_vento = coleta[6]
            precipitacao = coleta[7]

            # Prepara os dados para criar o objeto.
            data = datetime.datetime.strptime(data, '%d/%m/%Y')

            if not temperatura_min:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if coletas_corretas.get(anterior):
                        temperatura_min = coletas_corretas.get(anterior)['temperatura_min']
                        break

            if not temperatura_max:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if coletas_corretas.get(anterior):
                        temperatura_max = coletas_corretas.get(anterior)['temperatura_max']
                        break

            if not temperatura_media:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if coletas_corretas.get(anterior):
                        temperatura_media = coletas_corretas.get(anterior)['temperatura_media']
                        break

            if not umidade_media:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if coletas_corretas.get(anterior):
                        umidade_media = coletas_corretas.get(anterior)['umidade_media']
                        break

            if not insolacao:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if coletas_corretas.get(anterior):
                        insolacao = coletas_corretas.get(anterior)['insolacao']
                        break

            if not velocidade_vento:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if coletas_corretas.get(anterior):
                        velocidade_vento = coletas_corretas.get(anterior)['velocidade_vento']
                        break

            if not precipitacao:
                anterior = data
                while True:
                    anterior -= datetime.timedelta(days=1)
                    if coletas_corretas.get(anterior):
                        precipitacao = coletas_corretas.get(anterior)['precipitacao']
                        break

            try:
                temperatura_min = float(temperatura_min)
                temperatura_max = float(temperatura_max)
                temperatura_media = float(temperatura_media)
                umidade_media = float(umidade_media)
                insolacao = float(insolacao)
                velocidade_vento = float(velocidade_vento)
                precipitacao = float(precipitacao)

                writer.writerow([data.strftime('%d/%m/%Y'), temperatura_min, temperatura_max,
                    temperatura_media, umidade_media, insolacao,
                    velocidade_vento, precipitacao])

            except Exception, e:
                print 'Erro na data ', data
                print e

    except StopIteration:
        print '[2] Correção dos dados tratados realizada com sucesso.'
        arquivo_leitura.close()
        arquivo_escrita.close()


def criar_conjunto_treinamento_validacao():
    diretorio = os.path.dirname(__file__)
    arquivo_ct = open(
        os.path.join(diretorio, 'dados', 'conjunto_treinamento.csv'), 'wb')
    arquivo_cv = open(
        os.path.join(diretorio, 'dados', 'conjunto_validacao.csv'), 'wb')

    writer_ct = csv.writer(arquivo_ct, delimiter=';')
    # Escreve os cabeçalhos.
    writer_ct.writerow([
        'mes', 'temperatura_min1', 'temperatura_min2',
        'temperatura_max1', 'temperatura_max2', 'umidade_media1',
        'umidade_media2', 'insolacao1', 'insolacao2', 'velocidade_vento1',
        'velocidade_vento2', 'precipitacao', 'temperatura_min',
        'temperatura_max', 'umidade_media',
    ])

    writer_cv = csv.writer(arquivo_cv, delimiter=';')
    # Escreve os cabeçalhos.
    writer_cv.writerow([
        'mes', 'temperatura_min1', 'temperatura_min2',
        'temperatura_max1', 'temperatura_max2', 'umidade_media1',
        'umidade_media2', 'insolacao1', 'insolacao2', 'velocidade_vento1',
        'velocidade_vento2', 'precipitacao', 'temperatura_min',
        'temperatura_max', 'umidade_media',
    ])

    # Lê o arquivo com os dados e armazena os não defeituosos em um dicionário.
    todas_coletas = coletas_dict('dados_tratados_corrigidos.csv')

    quantidade = len(todas_coletas)

    # Serão 2000 elementos para treinamento e 2000 para validação.
    indices_treinamento = random.sample(xrange(2, quantidade, 1), tamanho_treinamento)
    indices_validacao = random.sample(xrange(2, quantidade, 1), tamanho_validacao)

    for i in indices_treinamento:

        coleta0 = todas_coletas.values()[i]
        coleta1 = todas_coletas.values()[i-1]
        coleta2 = todas_coletas.values()[i-2]

        # Dados da entrada.
        mes = todas_coletas.keys()[i].month
        temperatura_min1 = coleta1['temperatura_min']
        temperatura_min2 = coleta2['temperatura_min']
        temperatura_max1 = coleta1['temperatura_max']
        temperatura_max2 = coleta2['temperatura_max']
        umidade_media1 = coleta1['umidade_media']
        umidade_media2 = coleta2['umidade_media']
        insolacao1 = coleta1['insolacao']
        insolacao2 = coleta2['insolacao']
        velocidade_vento1 = coleta1['velocidade_vento']
        velocidade_vento2 = coleta2['velocidade_vento']
        # Dados da saída.
        precipitacao = coleta0['precipitacao']
        temperatura_min = coleta0['temperatura_min']
        temperatura_max = coleta0['temperatura_max']
        umidade_media = coleta0['umidade_media']

        writer_ct.writerow([
        mes, temperatura_min1, temperatura_min2,
        temperatura_max1, temperatura_max2, umidade_media1,
        umidade_media2, insolacao1, insolacao2, velocidade_vento1,
        velocidade_vento2, precipitacao, temperatura_min,
        temperatura_max, umidade_media,
        ])

    for i in indices_validacao:

        coleta0 = todas_coletas.values()[i]
        coleta1 = todas_coletas.values()[i-1]
        coleta2 = todas_coletas.values()[i-2]

        # Dados da entrada.
        mes = todas_coletas.keys()[i].month
        temperatura_min1 = coleta1['temperatura_min']
        temperatura_min2 = coleta2['temperatura_min']
        temperatura_max1 = coleta1['temperatura_max']
        temperatura_max2 = coleta2['temperatura_max']
        umidade_media1 = coleta1['umidade_media']
        umidade_media2 = coleta2['umidade_media']
        insolacao1 = coleta1['insolacao']
        insolacao2 = coleta2['insolacao']
        velocidade_vento1 = coleta1['velocidade_vento']
        velocidade_vento2 = coleta2['velocidade_vento']
        # Dados da saída.
        precipitacao = coleta0['precipitacao']
        temperatura_min = coleta0['temperatura_min']
        temperatura_max = coleta0['temperatura_max']
        umidade_media = coleta0['umidade_media']

        writer_cv.writerow([
        mes, temperatura_min1, temperatura_min2,
        temperatura_max1, temperatura_max2, umidade_media1,
        umidade_media2, insolacao1, insolacao2, velocidade_vento1,
        velocidade_vento2, precipitacao, temperatura_min,
        temperatura_max, umidade_media,
        ])

    arquivo_ct.close()
    arquivo_cv.close()
    print '[3] Criação dos conjuntos de treinamento e validação realizada com sucesso.'


#tratar_dados()
#corrigir_dados_tratados()
#criar_conjunto_treinamento_validacao()
