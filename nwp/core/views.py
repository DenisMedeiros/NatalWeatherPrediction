# -*- coding: utf-8 -*-

import os, csv, datetime, random, numpy
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .utils import tratamento_dados, dados_atuais, validacao, clima, fuzzy
from .models import Coleta
import datetime

# Create your views here.

class PaginaInicialView(View):

    def get(self, request):

        # Passa os dados para a RNA.
        hoje = datetime.datetime.now()
        ontem = hoje - datetime.timedelta(days=1)
        anteontem = hoje - datetime.timedelta(days=2)

        context = {
            'hoje': hoje,
        }

        coleta_ontem = Coleta.objects.get(data=ontem)
        coleta_anteontem = Coleta.objects.get(data=anteontem)

        previsao_hoje = validacao.executar(
            hoje.month,
            coleta_ontem.temperatura_min,
            coleta_anteontem.temperatura_min,
            coleta_ontem.temperatura_max,
            coleta_anteontem.temperatura_max,
            coleta_ontem.umidade_media,
            coleta_anteontem.umidade_media,
            coleta_ontem.insolacao,
            coleta_anteontem.insolacao,
            coleta_ontem.velocidade_vento,
            coleta_anteontem.velocidade_vento,
        )

        previsao_hoje['temperatura_min'] = round(previsao_hoje['temperatura_min'], 1)
        previsao_hoje['temperatura_max'] = round(previsao_hoje['temperatura_max'], 1)
        previsao_hoje['umidade_media'] = round(previsao_hoje['umidade_media'], 1)
        if previsao_hoje['precipitacao'] < 0:
            previsao_hoje['precipitacao'] = 0
        previsao_hoje['precipitacao'] = round(previsao_hoje['precipitacao'], 1)


        tempo_hoje = clima.get_tempo_hoje()

        confiabilidades = fuzzy.calcular_confiabilidade(
            previsao_hoje['precipitacao'], tempo_hoje['precipitacao'],
            previsao_hoje['temperatura_min'], tempo_hoje['temperatura_min'],
            previsao_hoje['temperatura_max'], tempo_hoje['temperatura_max'],
            previsao_hoje['umidade_media'], tempo_hoje['umidade_media'],
        )

        confiabilidades['conf_precipitacao'] = round(confiabilidades['conf_precipitacao'], 1)
        confiabilidades['conf_temp_min'] = round(confiabilidades['conf_temp_min'], 1)
        confiabilidades['conf_temp_max'] = round(confiabilidades['conf_temp_max'], 1)
        confiabilidades['conf_umidade_media'] = round(confiabilidades['conf_umidade_media'], 1)
       
        tempo_hoje['temperatura_min'] = round(tempo_hoje['temperatura_min'], 1)
        tempo_hoje['temperatura_max'] = round(tempo_hoje['temperatura_max'], 1)
        tempo_hoje['umidade_media'] = round(tempo_hoje['umidade_media'], 1)
        if tempo_hoje['precipitacao'] < 0:
            tempo_hoje['precipitacao'] = 0
        tempo_hoje['precipitacao'] = round(tempo_hoje['precipitacao'], 1)

        context.update({
            'precipitacao_real': tempo_hoje['precipitacao'],
            'temperatura_min_real': tempo_hoje['temperatura_min'],
            'temperatura_max_real': tempo_hoje['temperatura_max'],
            'umidade_media_real': tempo_hoje['umidade_media'],
        })


        context.update(previsao_hoje)
        context.update(confiabilidades)

        return render(request, 'pagina_inicial.html', context)

class SobreView(View):

    def get(self, request):
        context = {
        }
        return render(request, 'sobre.html', context)

class AtualizarDBView(View):
    
    def get(self, request):

        hoje = datetime.datetime.now()
        ontem = hoje - datetime.timedelta(days=1)

        if not Coleta.objects.filter(data=ontem).exists():
            atualizar_db()
            return HttpResponse("Banco de dados foi atualizado.")

        return HttpResponse("Banco de dados já está atualizado.")


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
            umidade_media = value['umidade_media'],
            insolacao = value['insolacao'],
            velocidade_vento = value['velocidade_vento'],
            precipitacao = value['precipitacao'],
        )

def atualizar_db():

    ultimas_coletas = dados_atuais.get()
   
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
            umidade_media = value['umidade_media'],
            insolacao = value['insolacao'],
            velocidade_vento = value['velocidade_vento'],
            precipitacao = value['precipitacao'],
        )

        print "Inserindo coleta do dia ", key