# -*- coding: utf-8 -*-

import json, requests

def get_tempo_hoje():
    
    url = 'http://api.wunderground.com/api/e71117b0df2e3a51/forecast/q/SBNT.json'

    resposta = requests.get(url=url)
    dados = json.loads(resposta.text)

    previsao_hoje = dados['forecast']['simpleforecast']['forecastday'][0]

    return {
        'precipitacao': float(previsao_hoje['qpf_allday']['mm']),
        'temperatura_min': float(previsao_hoje['low']['celsius']),
        'temperatura_max': float(previsao_hoje['high']['celsius']),
        'umidade_media': float(previsao_hoje['avehumidity']),
    }