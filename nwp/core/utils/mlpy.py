
# -*- coding: utf-8 -*-
# Author: Denis Medeiros
# Date: 30/Aug/2016

import numpy

'''
This is the Artificial Neural Network - Multi-layer perceptron training
algorithm using just one hidden layer, it uses the LMS as
optimization technique, and its activation function is the hyperbolic tangent.
Its parameters are the following ones:
* neurons_hidden_layer: Number of neurons in the hidden layer.
* break_error: Error when the learning should stop.
* break_iterations: Number of iterations when the learning should stop.
* eta: Learning factor.
* alpha: Momentum factor.
* input_data:  Input data (table form - see example.py).
* desired_output: Desired output (table form - see example.py).
The functions returns:
* hidden_layer_weights: Matrix (numpy array) with the weights of the hidden layer.
* output_layer_weights: Matrix (numpy array) with the weights of the output layer.
'''
def trainning_algorithm(
        neurons_hidden_layer,
        break_error,
        break_iterations,
        eta,
        alpha,
        input_data,
        desired_output,
):

    # Reorganize the input and output data.to their transposed form.
    input_data = input_data.T
    desired_output = desired_output.T

    # Get details about the input and output.

    input_size, number_entries =  input_data.shape
    output_size, _ = desired_output.shape

    # Define the weights matrices.
    hidden_layer_weights = numpy.random.random(
                                        (neurons_hidden_layer, input_size+1)
    )
    output_layer_weights = numpy.random.random(
                                        (output_size, neurons_hidden_layer+1)
    )

    # Define the deltas used in the back progapation algorithm.
    previous_delta_hidden_layer  = numpy.zeros(
                                        (neurons_hidden_layer, input_size+1)
    )
    previous_delta_output_layer_layer = numpy.zeros(
                                        (output_size, neurons_hidden_layer+1)
    )

    # Add the bias to the input matrix.
    input_data_bias = numpy.vstack(
                            (numpy.full((1, number_entries), -1.0), input_data)
    )

    iterations = 0
    while True:

        # Shuffle the input order to improve the learning.
        new_order = numpy.random.permutation(number_entries)
        input_data_bias = input_data_bias[:, new_order]
        desired_output = desired_output[:, new_order]

        # Find the output of the hidden layer.
        hidden_layer_output = numpy.tanh(hidden_layer_weights.dot(input_data_bias))

        # Add the bias to the hidden layer output.
        hidden_layer_output_bias = numpy.vstack(
                            (numpy.full(
                                (1, number_entries), -1.0), hidden_layer_output
                            )
        )

        # Find the output of the output layer.
        final_output = numpy.tanh(
                                output_layer_weights.dot(hidden_layer_output_bias)
        )

        # Calculate the static error.
        static_error = desired_output - final_output

        # Execute the back propagation algorithm.
        delta_output_layer_temp = numpy.multiply(
                    1.0 - numpy.square(numpy.tanh(final_output)), static_error
        )

        delta_output_layer = (
                    (eta/number_entries) *
                    delta_output_layer_temp.dot(
                        hidden_layer_output_bias.T
                    )
        ) + alpha * previous_delta_output_layer_layer;

        previous_delta_output_layer_layer = delta_output_layer
        output_layer_weights = output_layer_weights + delta_output_layer

        delta_hidden_layer_temp = numpy.multiply(
            1 - numpy.square(numpy.tanh(hidden_layer_output_bias)),
            numpy.dot(output_layer_weights.T, delta_output_layer_temp)
        )

        delta_hidden_layer_temp_2 = delta_hidden_layer_temp[1:neurons_hidden_layer+1, :]

        delta_hidden_layer = (
                    (eta/number_entries) *
                    delta_hidden_layer_temp_2.dot(input_data_bias.T)
                )+ alpha * previous_delta_hidden_layer;

        previous_delta_hidden_layer = delta_hidden_layer
        hidden_layer_weights = hidden_layer_weights + delta_hidden_layer

        # Calculate the total error.
        total_error = (
                (1.0/(2.0 * number_entries)) *
                numpy.trace(static_error.T.dot(static_error))
        )

        if total_error < break_error or iterations >= break_iterations:
            break


        print 'Iteracao %d, Erro %.20f' %(iterations, total_error)
        iterations += 1

    # Return the weights.
    print "\n----- End of the training ------\n"
    print "Final error:", total_error * 10, "%"
    print "Number of iterations:", iterations
    print "\n----- End of the training ------\n"

    return (hidden_layer_weights, output_layer_weights)

'''
This is the Artificial Neural Network - Multi-layer perceptron validating
algorithm using just one hidden layer.
Its parameters are the following ones:
* hidden_layer_weights: Matrix with the weights of the hidden layer.
* output_layer_weights: Matrix with the weights of the output layer.
* input_data: Input data (table form - see example.py).
The functions returns:
* final_output: The output related to that input data.
'''
def validating_algorithm(
    hidden_layer_weights, # Weights of the hidden layer.
    output_layer_weights, # Weights of the output layer.
    input_data, # Input data (table format).
):
    # Reorganize the input data.
    input_data = input_data.T
    input_size, number_entries =  input_data.shape

    # Add the bias to the input matrix.
    input_data_bias = numpy.vstack(
                            (numpy.full((1, number_entries), -1.0), input_data)
    )

    # Find the output of the hidden layer.
    hidden_layer_output = numpy.tanh(hidden_layer_weights.dot(input_data_bias))

    hidden_layer_output_bias = numpy.vstack(
                    (numpy.full((1, number_entries), -1.0), hidden_layer_output)
    )

    # Find the output of the output layer.
    final_output = numpy.tanh(output_layer_weights.dot(hidden_layer_output_bias))

    return final_output
