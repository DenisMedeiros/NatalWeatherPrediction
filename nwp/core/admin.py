# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Coleta, Previsao

@admin.register(Coleta)
class ColetaAdmin(admin.ModelAdmin):
    list_display = ('data', 'temperatura_max', 'temperatura_min',
        'temperatura_media', 'umidade_media', 'velocidade_vento',)
    ordering = ('-data',)
    #list_filter = ('data', 'temperatura_max', 'temperatura_min',
    #    'temperatura_media', 'umidade_media', 'velocidade_vento',)
    #search_fields = ('username', 'first_name',)

@admin.register(Previsao)
class PrevisaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'temperatura_max', 'temperatura_min',
        'umidade_media', 'precipitacao',)
    ordering = ('-data',)
    #list_filter = ('data', 'temperatura_max', 'temperatura_min',
    #    'temperatura_media', 'umidade_media', 'velocidade_vento',)
    #search_fields = ('username', 'first_name',)