#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, math, os
from sklearn.neural_network import MLPClassifier, MLPRegressor

diretorio = os.path.dirname(__file__)
arquivo_leitura = open(
os.path.join(diretorio, 'conjunto_treinamento.csv'), 'rb')

reader = csv.reader(arquivo_leitura, delimiter=';')

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
        humidade_media1 = float(linha[5])
        humidade_media2 = float(linha[6])
        insolacao1 = float(linha[7])
        insolacao2 = float(linha[8])
        velocidade_vento1 = float(linha[9])
        velocidade_vento2 = float(linha[10])

        # Dados da saída.
        precipitacao = float(linha[11])
        temperatura_min = float(linha[12])
        temperatura_max = float(linha[13])
        humidade_media = float(linha[14])

        entradas.append([mes, temperatura_min1, temperatura_min2,
            temperatura_max1, temperatura_max2, humidade_media1,
            humidade_media2, insolacao1, insolacao2, velocidade_vento1,
            velocidade_vento2,])

        saidas.append([precipitacao, temperatura_min, 
            temperatura_max, humidade_media,])

except StopIteration:
    arquivo_leitura.close()


# Realiza o treitamento.

'''
Regressor MLP.
Parâmetros importantes:
http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor
'''
reg = MLPRegressor(
    solver='adam', 
    activation='tanh', 
    learning_rate='adaptive',
    max_iter=1000, 
    alpha=1e-6,
    hidden_layer_sizes=(32,), 
    random_state=1,
    learning_rate_init=0.1,
    shuffle=True,
    momentum=0.01,
    tol=1e-6,
    #beta_1=0.9,
    #beta_2=0.999,
    #epsilon=1e-8,
    early_stopping=False,
    verbose=True,
)

reg.fit(entradas, saidas)   


print [coef.shape for coef in reg.coefs_]


# Faz a validação.
indices = [10, 100, 1000]
for i in indices:
    print 'Original: ', saidas[i]
    print 'Calculado: ', reg.predict([entradas[i]])
