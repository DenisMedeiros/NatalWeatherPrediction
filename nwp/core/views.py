# -*- coding: utf-8 -*-

import os, csv, datetime, random, numpy
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .utils import tratamento_dados, dados_atuais
from .models import Coleta
import datetime

# Create your views here.

class PaginaInicialView(View):

    def get(self, request):
        context = {
            'hoje': datetime.datetime.now(),
        }
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