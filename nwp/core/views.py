# -*- coding: utf-8 -*-

import os, csv, datetime, random, numpy
from django.shortcuts import render
from django.views.generic import View
from .utils import tratamento_dados
from .models import Coleta

# Create your views here.

class PaginaInicialView(View):

    def get(self, request):
        #popular_db()
        context = {
            'hoje': datetime.datetime.now(),
        }
        return render(request, 'pagina_inicial.html', context)

class SobreView(View):

    def get(self, request):
        context = {
        }
        return render(request, 'sobre.html', context)


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
