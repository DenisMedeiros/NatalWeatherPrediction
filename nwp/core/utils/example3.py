#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy, csv, math
from mlpy import *

from sklearn.neural_network import MLPClassifier
X = [
    [0., 0.], 
    [0., 1.],
    [1., 0.],
    [1., 1.],
]
Y = [0, 1, 1, 0,]


'''
Classificador MLP.
Parâmetros importantes:
    activation : {‘identity’, ‘logistic’, ‘tanh’, ‘relu’}, default ‘relu’
    solver : {‘lbfgs’, ‘sgd’, ‘adam’}, default ‘adam’
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


# Realiza o treinamento.
clf.fit(X, Y)    

# Faz uma predição.
resultado = clf.predict([
    [0., 0.], 
    [0., 1.],
    [1., 0.],
    [1., 1.],
])  


#print   

#print [coef.shape for coef in clf.coefs_]