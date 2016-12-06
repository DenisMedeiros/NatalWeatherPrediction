# -*- coding: utf-8 -*-

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def calcular_confiabilidade(
        prec_rna, prec_real,
        temp_min_rna, temp_min_real,
        temp_max_rna, temp_max_real,
        um_media_rna, um_media_real,
    ):

    ''' Funções de pertinência dos antecedentes (entradas). '''

    precipitacao_rna = ctrl.Antecedent(np.arange(-1, 302, 1), 'precipitacao_rna')
    precipitacao_real = ctrl.Antecedent(np.arange(1, 302, 1), 'precipitacao_real')

    precipitacao_rna['baixo'] = fuzz.trimf(precipitacao_rna.universe, [-1, 15, 30])
    precipitacao_rna['medio'] = fuzz.trimf(precipitacao_rna.universe, [20, 40, 60])
    precipitacao_rna['alto'] = fuzz.trimf(precipitacao_rna.universe, [50, 175, 301])

    precipitacao_real['baixo'] = fuzz.trimf(precipitacao_real.universe, [-1, 15, 30])
    precipitacao_real['medio'] = fuzz.trimf(precipitacao_real.universe, [20, 40, 60])
    precipitacao_real['alto'] = fuzz.trimf(precipitacao_real.universe, [50, 175, 301])

    #precipitacao_rna['baixo'].view()

    temperatura_min_rna = ctrl.Antecedent(np.arange(-1, 42, 1), 'temperatura_min_rna')
    temperatura_min_real = ctrl.Antecedent(np.arange(-1, 42, 1), 'temperatura_min_real')

    temperatura_min_rna['baixo'] = fuzz.trimf(temperatura_min_rna.universe, [-1, 10, 20])
    temperatura_min_rna['medio'] = fuzz.trimf(temperatura_min_rna.universe, [10, 23, 35])
    temperatura_min_rna['alto'] = fuzz.trimf(temperatura_min_rna.universe, [25, 33, 41])

    temperatura_min_real['baixo'] = fuzz.trimf(temperatura_min_real.universe, [-1, 10, 20])
    temperatura_min_real['medio'] = fuzz.trimf(temperatura_min_real.universe, [10, 23, 35])
    temperatura_min_real['alto'] = fuzz.trimf(temperatura_min_real.universe, [25, 33, 41])

    #temperatura_min_rna['baixo'].view()
   

    temperatura_max_rna = ctrl.Antecedent(np.arange(-1, 42, 1), 'temperatura_max_rna')
    temperatura_max_real = ctrl.Antecedent(np.arange(-1, 42, 1), 'temperatura_max_real')

    temperatura_max_rna['baixo'] = fuzz.trimf(temperatura_max_rna.universe, [-1, 10, 20])
    temperatura_max_rna['medio'] = fuzz.trimf(temperatura_max_rna.universe, [10, 23, 35])
    temperatura_max_rna['alto'] = fuzz.trimf(temperatura_max_rna.universe, [25, 33, 41])

    temperatura_max_real['baixo'] = fuzz.trimf(temperatura_max_real.universe, [-1, 10, 20])
    temperatura_max_real['medio'] = fuzz.trimf(temperatura_max_real.universe, [10, 23, 35])
    temperatura_max_real['alto'] = fuzz.trimf(temperatura_max_real.universe, [25, 33, 41])

    #temperatura_max_rna['baixo'].view()

    umidade_media_rna = ctrl.Antecedent(np.arange(-1, 102, 1), 'umidade_media_rna')
    umidade_media_real = ctrl.Antecedent(np.arange(-1, 102, 1), 'umidade_media_real') 

    umidade_media_rna['baixo'] = fuzz.trimf(umidade_media_rna.universe, [-1, 25, 50])
    umidade_media_rna['medio'] = fuzz.trimf(umidade_media_rna.universe, [20, 50, 80])
    umidade_media_rna['alto'] = fuzz.trimf(umidade_media_rna.universe, [50, 75, 101])

    umidade_media_real['baixo'] = fuzz.trimf(umidade_media_real.universe, [-1, 25, 50])
    umidade_media_real['medio'] = fuzz.trimf(umidade_media_real.universe, [20, 50, 80])
    umidade_media_real['alto'] = fuzz.trimf(umidade_media_real.universe, [50, 75, 101])

    #umidade_media_rna['baixo'].view()
    #input()

    ''' Funções de pertinência dos consequentes (saídas). '''
    conf_precipitacao = ctrl.Consequent(np.arange(-1, 102, 1), 'conf_precipitacao')

    conf_precipitacao['baixo'] = fuzz.trimf(conf_precipitacao.universe, [-1, 20, 40])
    conf_precipitacao['medio'] = fuzz.trimf(conf_precipitacao.universe, [20, 50, 80])
    conf_precipitacao['alto'] = fuzz.trimf(conf_precipitacao.universe, [60, 80, 101])

    conf_temp_min = ctrl.Consequent(np.arange(-1, 102, 1), 'conf_temp_min')

    conf_temp_min['baixo'] = fuzz.trimf(conf_temp_min.universe, [-1, 20, 40])
    conf_temp_min['medio'] = fuzz.trimf(conf_temp_min.universe, [20, 50, 80])
    conf_temp_min['alto'] = fuzz.trimf(conf_temp_min.universe, [60, 80, 101])

    conf_temp_max = ctrl.Consequent(np.arange(-1, 102, 1), 'conf_temp_max')

    conf_temp_max['baixo'] = fuzz.trimf(conf_temp_max.universe, [-1, 20, 40])
    conf_temp_max['medio'] = fuzz.trimf(conf_temp_max.universe, [20, 50, 80])
    conf_temp_max['alto'] = fuzz.trimf(conf_temp_max.universe, [60, 80, 101])

    conf_umidade_media= ctrl.Consequent(np.arange(-1, 102, 1), 'conf_umidade_media')

    conf_umidade_media['baixo'] = fuzz.trimf(conf_umidade_media.universe, [-1, 20, 40])
    conf_umidade_media['medio'] = fuzz.trimf(conf_umidade_media.universe, [20, 50, 80])
    conf_umidade_media['alto'] = fuzz.trimf(conf_umidade_media.universe, [60, 80, 100])

    ''' Regras '''
    regras_precipitacao = [
        ctrl.Rule(
            precipitacao_rna['baixo'] & precipitacao_real['baixo'], 
            conf_precipitacao['alto'],
        ),
        ctrl.Rule(
            precipitacao_rna['medio'] & precipitacao_real['medio'], 
            conf_precipitacao['alto'],
        ),
        ctrl.Rule(
            precipitacao_rna['alto'] & precipitacao_real['alto'], 
            conf_precipitacao['alto'],
        ),
        ctrl.Rule(
            precipitacao_rna['baixo'] & precipitacao_real['medio'], 
            conf_precipitacao['medio'],
        ),
        ctrl.Rule(
            precipitacao_rna['medio'] & precipitacao_real['baixo'], 
            conf_precipitacao['medio'],
        ),
        ctrl.Rule(
            precipitacao_rna['medio'] & precipitacao_real['alto'], 
            conf_precipitacao['medio'],
        ),
        ctrl.Rule(
            precipitacao_rna['alto'] & precipitacao_real['medio'], 
            conf_precipitacao['medio'],
        ),
        ctrl.Rule(
            precipitacao_rna['baixo'] & precipitacao_real['alto'], 
            conf_precipitacao['baixo'],
        ),
        ctrl.Rule(
            precipitacao_rna['alto'] & precipitacao_real['baixo'], 
            conf_precipitacao['baixo'],
        ),
    ]

    regras_temperatura_min = [
        ctrl.Rule(
            temperatura_min_rna['baixo'] & temperatura_min_real['baixo'], 
            conf_temp_min['alto'],
        ),
        ctrl.Rule(
            temperatura_min_rna['medio'] & temperatura_min_real['medio'], 
            conf_temp_min['alto'],
        ),
        ctrl.Rule(
            temperatura_min_rna['alto'] & temperatura_min_real['alto'], 
            conf_temp_min['alto'],
        ),
        ctrl.Rule(
            temperatura_min_rna['baixo'] & temperatura_min_real['medio'], 
            conf_temp_min['medio'],
        ),
        ctrl.Rule(
            temperatura_min_rna['medio'] & temperatura_min_real['baixo'], 
            conf_temp_min['medio'],
        ),
        ctrl.Rule(
            temperatura_min_rna['medio'] & temperatura_min_real['alto'], 
            conf_temp_min['medio'],
        ),
        ctrl.Rule(
            temperatura_min_rna['alto'] & temperatura_min_real['medio'], 
            conf_temp_min['medio'],
        ),
        ctrl.Rule(
            temperatura_min_rna['baixo'] & temperatura_min_real['alto'], 
            conf_temp_min['baixo'],
        ),
        ctrl.Rule(
            temperatura_min_rna['alto'] & temperatura_min_real['baixo'], 
            conf_temp_min['baixo'],
        ),
    ]

    regras_temperatura_max = [
        ctrl.Rule(
            temperatura_max_rna['baixo'] & temperatura_max_real['baixo'], 
            conf_temp_max['alto'],
        ),
        ctrl.Rule(
            temperatura_max_rna['medio'] & temperatura_max_real['medio'], 
            conf_temp_max['alto'],
        ),
        ctrl.Rule(
            temperatura_max_rna['alto'] & temperatura_max_real['alto'], 
            conf_temp_max['alto'],
        ),
        ctrl.Rule(
            temperatura_max_rna['baixo'] & temperatura_max_real['medio'], 
            conf_temp_max['medio'],
        ),
        ctrl.Rule(
            temperatura_max_rna['medio'] & temperatura_max_real['baixo'], 
            conf_temp_max['medio'],
        ),
        ctrl.Rule(
            temperatura_max_rna['medio'] & temperatura_max_real['alto'], 
            conf_temp_max['medio'],
        ),
        ctrl.Rule(
            temperatura_max_rna['alto'] & temperatura_max_real['medio'], 
            conf_temp_max['medio'],
        ),
        ctrl.Rule(
            temperatura_max_rna['baixo'] & temperatura_max_real['alto'], 
            conf_temp_max['baixo'],
        ),
        ctrl.Rule(
            temperatura_max_rna['alto'] & temperatura_max_real['baixo'], 
            conf_temp_max['baixo'],
        ),
    ]

    regras_umidade_media = [
        ctrl.Rule(
            umidade_media_rna['baixo'] & umidade_media_real['baixo'], 
            conf_umidade_media['alto'],
        ),
        ctrl.Rule(
            umidade_media_rna['medio'] & umidade_media_real['medio'], 
            conf_umidade_media['alto'],
        ),
        ctrl.Rule(
            umidade_media_rna['alto'] & umidade_media_real['alto'], 
            conf_umidade_media['alto'],
        ),
        ctrl.Rule(
            umidade_media_rna['baixo'] & umidade_media_real['medio'], 
            conf_umidade_media['medio'],
        ),
        ctrl.Rule(
            umidade_media_rna['medio'] & umidade_media_real['baixo'], 
            conf_umidade_media['medio'],
        ),
        ctrl.Rule(
            umidade_media_rna['medio'] & umidade_media_real['alto'], 
            conf_umidade_media['medio'],
        ),
        ctrl.Rule(
            umidade_media_rna['alto'] & umidade_media_real['medio'], 
            conf_umidade_media['medio'],
        ),
        ctrl.Rule(
            umidade_media_rna['baixo'] & umidade_media_real['alto'], 
            conf_umidade_media['baixo'],
        ),
        ctrl.Rule(
            umidade_media_rna['alto'] & umidade_media_real['baixo'], 
            conf_umidade_media['baixo'],
        ),
    ]

    ''' Execução da máquina de inferência '''
    confiabilidade_ctrl = ctrl.ControlSystem(
        regras_precipitacao + 
        regras_temperatura_min + 
        regras_temperatura_max + 
        regras_umidade_media
    )
    confiabilidade = ctrl.ControlSystemSimulation(confiabilidade_ctrl)

    confiabilidade.input['precipitacao_rna'] = prec_rna
    confiabilidade.input['precipitacao_real'] = prec_real
    confiabilidade.input['temperatura_min_rna'] = temp_min_rna
    confiabilidade.input['temperatura_min_real'] = temp_min_real
    confiabilidade.input['temperatura_max_rna'] = temp_max_rna
    confiabilidade.input['temperatura_max_real'] = temp_max_real
    confiabilidade.input['umidade_media_rna'] = um_media_rna
    confiabilidade.input['umidade_media_real'] = um_media_real

    # Calcula
    confiabilidade.compute()

    #print confiabilidade.input
    #print confiabilidade.output
    #conf_precipitacao.view(sim=confiabilidade)

    print confiabilidade.output
    return confiabilidade.output


'''print calcular_confiabilidade(
        prec_rna=1, prec_real=5,
        temp_min_rna=22, temp_min_real=25,
        temp_max_rna=31, temp_max_real=33,
        um_media_rna=60, um_media_real=65,
)'''