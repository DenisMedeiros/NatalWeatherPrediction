#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os, random, numpy
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.externals import joblib

def testar_conjunto_validacao():
    diretorio = os.path.dirname(__file__)
    arquivo_leitura = open(
    os.path.join(diretorio, 'dados', 'conjunto_validacao.csv'), 'rb')

    reader = csv.reader(arquivo_leitura, delimiter=';')
    reader.next()

    entradas = []
    saidas = []

    # Prepara as entradas e saídas.
    try:
        while True:
            linha = reader.next()

            # Dados da entrada.
            mes = float(linha[0])
            temperatura_min1 = float(linha[1])
            temperatura_min2 = float(linha[2])
            temperatura_max1 = float(linha[3])
            temperatura_max2 = float(linha[4])
            umidade_media1 = float(linha[5])
            umidade_media2 = float(linha[6])
            insolacao1 = float(linha[7])
            insolacao2 = float(linha[8])
            velocidade_vento1 = float(linha[9])
            velocidade_vento2 = float(linha[10])

            # Dados da saída.
            precipitacao = float(linha[11])
            temperatura_min = float(linha[12])
            temperatura_max = float(linha[13])
            umidade_media = float(linha[14])

            entradas.append([mes, temperatura_min1, temperatura_min2,
                temperatura_max1, temperatura_max2, umidade_media1,
                umidade_media2, insolacao1, insolacao2, velocidade_vento1,
                velocidade_vento2,])

            saidas.append([precipitacao, temperatura_min,
                temperatura_max, umidade_media,])

    except StopIteration:
        arquivo_leitura.close()

    # Carrega o conhecimento obtido de um treinamento anterior.
    reg = joblib.load(os.path.join(diretorio, 'conhecimento.pkl'))

    for i in range(len(entradas)):
        saida_rna = reg.predict([entradas[i]])
        saida_esperada = saidas[i]

        print 'Saída esperada: ', [saida_esperada]
        print 'Saída da RNA: ', numpy.round(saida_rna, decimals=1)
        print '-----'

def executar(
            mes, 
            temperatura_min1,
            temperatura_min2,
            temperatura_max1,
            temperatura_max2,
            umidade_media1,
            umidade_media2 ,
            insolacao1,
            insolacao2,
            velocidade_vento1,
            velocidade_vento2,):

    diretorio = os.path.dirname(__file__)
    # Carrega o conhecimento obtido de um treinamento anterior.
    reg = joblib.load(os.path.join(diretorio, 'conhecimento.pkl'))
    saida_rna = reg.predict([[mes, temperatura_min1, temperatura_min2,
                temperatura_max1, temperatura_max2, umidade_media1,
                umidade_media2, insolacao1, insolacao2, velocidade_vento1,
                velocidade_vento2,]])

    return {
            'precipitacao': saida_rna[0][0],
            'temperatura_min': saida_rna[0][1],
            'temperatura_max': saida_rna[0][2],
            'umidade_media': saida_rna[0][3],
            }

