# -*- coding: utf-8 -*-

import pyowm

def get_tempo_hoje():
    owm = pyowm.OWM('10477b205f26c621bd1473b9660d791b')  # You MUST provide a valid API key
    obs = owm.weather_at_id(3394023)
    data = obs.get_reception_time(timeformat='date') 
    w = obs.get_weather()
    precipitacoes = w.get_rain()  
    temperaturas = w.get_temperature(unit='celsius')  
    umidade = w.get_humidity()    

    if precipitacoes:
        precipitacao = precipitacoes['3h']
    else:
        precipitacao = 0

    temperatura_min = temperaturas['temp_min']
    temperatura_max = temperaturas['temp_max']
    umidade_media = umidade

    return {
        'precipitacao': precipitacao,
        'temperatura_min': temperatura_min,
        'temperatura_max': temperatura_max,
        'umidade_media': umidade_media,
    }