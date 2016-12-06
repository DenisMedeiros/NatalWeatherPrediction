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


#entradas = numpy.array(entradas)
#saidas = numpy.array(saidas)

X = [
    [0., 0.], 
    [0., 1.],
    [1., 0.],
    [1., 1.],
]


Y = [[10.,10.,10.], [10.,20.,20.], [10.,20.,20.], [20.,20.,10.],]

X = entradas
Y = saidas


'''
X = []
Y = []
for i in range(-10,10,1):
    X.append([float(i)])
    Y.append([float(2*i)])

X = numpy.array(X)
Y = numpy.array(Y)

Y_normalized = normalize(Y, norm='l2')


print X.shape
print Y.shape
'''

'''
Classificador MLP.
Parâmetros importantes:
    activation : {'identity', 'logistic', 'tanh', 'relu'}, default 'relu'
    solver : {'lbfgs', 'sgd', 'adam'}, default 'adam'
'''
'''
clf = MLPClassifier(
    solver='lbfgs', 
    activation='tanh', 
    max_iter=1000, 
    alpha=1e-2,
    hidden_layer_sizes=(16,), 
    random_state=1,
    #learning_rate_init=0.1,
    #shuffle=True,
    #momentum=0.9,
    #beta_1=0.9,
    #beta_2=0.999,
    #epsilon=1e-8,
    #early_stopping=True,
    #verbose=True,
)
'''

'''
Regressor MLP.
Parâmetros importantes:
    activation : {'identity', 'logistic', 'tanh', 'relu'}, default 'relu'
    solver : {'lbfgs', 'sgd', 'adam'}, default 'adam'
'''
reg = MLPRegressor(
    solver='lbfgs', 
    activation='tanh', 
    max_iter=1000, 
    alpha=1e-5,
    hidden_layer_sizes=(16,), 
    random_state=1,
    learning_rate_init=0.1,
    shuffle=True,
    momentum=0.9,
    #beta_1=0.9,
    #beta_2=0.999,
    #epsilon=1e-8,
    #early_stopping=True,
    verbose=True,
)

'''
# Realiza o treinamento.
clf.fit(X, Y_normalized)    

# Faz uma predição.
resultado = clf.predict([
    [0., 0.], 
    [0., 1.],
    [1., 0.],
    [1., 1.],
])  

print resultado


#print   

#print [coef.shape for coef in clf.coefs_]
'''

reg.fit(X, Y)   

'''
# Faz uma predição.
resultado = reg.predict([
    [0., 0.], 
    [0., 1.],
    [1., 0.],
    [1., 1.],
])  
'''


#resultado = normalize(resultado_norm, norm='l2', return_norm=True)
#print resultado