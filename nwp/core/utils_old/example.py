#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy, csv
from mlpy import *

'''
A entrada da RNA será no formato a seguir:
[
    mes,

    temp_min_1,
    temp_max_1,
    humidade_media_1,
    insolacao_1,
    velocidade_vento_1,

    temp_min_2,
    temp_max_2,
    humidade_media_2,
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
    humidade,
]
'''
desired_output = numpy.array([
    [-1],
    [1],
    [1],
    [-1],
])

# Run the training algorithm.
(hidden_weights, output_weights) = trainning_algorithm(
    neurons_hidden_layer = 8,
    break_error = 1e-2,
    break_iterations = 1000000,
    eta = 0.1,
    alpha = 0.3,
    input_data = input_data,
    desired_output = desired_output
)

test_data = numpy.matrix([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
])

result = validating_algorithm(hidden_weights, output_weights, test_data)
print numpy.transpose(result)
