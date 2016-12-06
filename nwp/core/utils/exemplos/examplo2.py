#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy, csv, math
from mlpy import *

'''
A entrada da RNA será no formato a seguir:
[
    mes,

    temp_min_1,
    temp_max_1,
    umidade_media_1,
    insolacao_1,
    velocidade_vento_1,

    temp_min_2,
    temp_max_2,
    umidade_media_2,
    insolacao_2,
    velocidade_vento_2,

]
'''
input_data = numpy.array([
    [0,0],
    [0,1],
    [1,0],
    [1,1],
])


'''
A saída da RNA será no formato a seguir:
[
    precipitacao,
    temp_min,
    temp_max,
    umidade,
]
'''
desired_output = numpy.array([
    [0],
    [1],
    [1],
    [1],
])


entrada = []
saida = []
for i in range(1, 20, 1):
    entrada.append([i])
    saida.append([i*2])

input_data = numpy.array(entrada)
desired_output = numpy.array(saida)


do_max = numpy.amax(desired_output)
do_min = numpy.amin(desired_output)
delta = float(do_max-do_min) 
do_norm = ((desired_output - do_min)/delta - 0.5 ) * 2.0;

# Run the training algorithm.
(hidden_weights, output_weights) = trainning_algorithm(
    neurons_hidden_layer = 32,
    break_error = 1e-6,
    break_iterations = 1000000,
    eta = 0.2,
    alpha = 0.7,
    input_data = input_data,
    desired_output = do_norm
)


test_data = numpy.matrix([
    [5],
    [3],
    [2],
    [1],
])

result_norm = validating_algorithm(hidden_weights, output_weights, input_data)

result = (result_norm/2.0 + 0.5) * (delta) + do_min;

print numpy.transpose(result)