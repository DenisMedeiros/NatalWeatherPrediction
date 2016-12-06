#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os, random
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.externals import joblib

diretorio = os.path.dirname(__file__)
arquivo_leitura = open(
os.path.join(diretorio, 'dados', 'conjunto_treinamento.csv'), 'rb')

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


# Realiza o treitamento.

'''
Regressor MLP.
Parâmetros importantes:
http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor
'''
reg = MLPRegressor(
    solver='lbfgs',
    activation='tanh',
    learning_rate='constant',
    max_iter=200000,
    alpha=1e-5,
    warm_start=False,
    hidden_layer_sizes=(200,),
    #random_state = random.randint(0,4294967295),
    tol=1e-8,
    verbose=True,
    learning_rate_init=0.01, # Usado no sgd.
    shuffle=True, # Usado no sgd ou adam.
    momentum=0.1, # Usado no sgd.
    nesterovs_momentum=True, # Usado no sgd.
    power_t = 0.5, # Usado no sgd.
    beta_1=0.9, # Usado no adam.
    beta_2=0.999, # Usado no adam.
    epsilon=1e-8, # Usado no adam.
    early_stopping=False, #  Usado no adam ou sgd.
    validation_fraction=0.1, #  Usado no adam ou sgd.
    batch_size=200, #  Usado no adam ou sgd.
)

reg.fit(entradas, saidas)

# Salva em disco o treinamento realizado.
joblib.dump(reg, os.path.join(diretorio, 'conhecimento.pkl'))

print "Treinamento concluído após %d iterações." %(reg.n_iter_)
