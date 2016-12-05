# -*- coding: utf-8 -*-

import os, csv, datetime, random, numpy
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .utils import tratamento_dados, dados_atuais, validacao
from .models import Coleta
import datetime

# Create your views here.

class PaginaInicialView(View):

    def get(self, request):

        # Passa os dados para a RNA.
        hoje = datetime.datetime.now()
        ontem = hoje - datetime.timedelta(days=1)
        anteontem = hoje - datetime.timedelta(days=2)

        coleta_ontem = Coleta.objects.get(data=ontem)
        coleta_anteontem = Coleta.objects.get(data=anteontem)

        previsao_hoje = validacao.executar(
            hoje.month,
            coleta_ontem.temperatura_min,
            coleta_anteontem.temperatura_min,
            coleta_ontem.temperatura_max,
            coleta_anteontem.temperatura_max,
            coleta_ontem.humidade_media,
            coleta_anteontem.humidade_media,
            coleta_ontem.insolacao,
            coleta_anteontem.insolacao,
            coleta_ontem.velocidade_vento,
            coleta_anteontem.velocidade_vento,
        )

        previsao_hoje['temperatura_min'] = round(previsao_hoje['temperatura_min'], 1)
        previsao_hoje['temperatura_max'] = round(previsao_hoje['temperatura_max'], 1)
        previsao_hoje['humidade_media'] = round(previsao_hoje['humidade_media'], 1)
        if previsao_hoje['precipitacao'] < 0:
            previsao_hoje['precipitacao'] = 0
        previsao_hoje['precipitacao'] = round(previsao_hoje['precipitacao'], 1)

        context = {
            'hoje': hoje,
        }

        context.update(previsao_hoje)
        return render(request, 'pagina_inicial.html', context)

class SobreView(View):

    def get(self, request):
        context = {
        }
        return render(request, 'sobre.html', context)

class AtualizarDBView(View):
    
    def get(self, request):
        atualizar_db()
        context = {
        }
        return HttpResponse("BD atualizado.")


# Função auxiliar.

'''
Insere no banco de dados os dados tratados.
'''
def popular_db():

    todas_coletas = tratamento_dados.coletas_dict('dados_tratados_corrigidos.csv')

    for key, value in todas_coletas.iteritems():
        print "Inserindo coleta do dia ", key
        Coleta.objects.get_or_create(
            data = key,
            temperatura_min = value['temperatura_min'],
            temperatura_max = value['temperatura_max'],
            temperatura_media = value['temperatura_media'],
            humidade_media = value['humidade_media'],
            insolacao = value['insolacao'],
            velocidade_vento = value['velocidade_vento'],
            precipitacao = value['precipitacao'],
        )

def atualizar_db():

    #ultimas_coletas = dados_atuais.get()
    ultimas_coletas = {datetime.datetime(2016, 12, 3, 0, 0): {'velocidade_vento': 3.1, 'temperatura_media': 'erro', 'temperatura_min': 'erro', 'insolacao': 11.0, 'temperatura_max': 30.0, 'humidade_media': 71.0, 'precipitacao': 0.0}, datetime.datetime(2016, 12, 4, 0, 0): {'velocidade_vento': 2.6, 'temperatura_media': 'erro', 'temperatura_min': 'erro', 'insolacao': 10.1, 'temperatura_max': 30.0, 'humidade_media': 71.0, 'precipitacao': 0.0}}
    
    # Substitui todos os campos com erro com os da última data válida.
    for key, value in ultimas_coletas.iteritems():
        for key2, value2 in value.iteritems():
            if value2 == 'erro':    
                ultima_coleta_valida = Coleta.objects.latest('data')
                ultimas_coletas[key][key2] = getattr(ultima_coleta_valida, key2)

    # Insere no BD as coletas.
    for key, value in ultimas_coletas.iteritems():
        Coleta.objects.get_or_create(
            data = key,
            temperatura_min = value['temperatura_min'],
            temperatura_max = value['temperatura_max'],
            temperatura_media = value['temperatura_media'],
            humidade_media = value['humidade_media'],
            insolacao = value['insolacao'],
            velocidade_vento = value['velocidade_vento'],
            precipitacao = value['precipitacao'],
        )

        print "Inserindo coleta do dia ", key