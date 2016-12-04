# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Coleta

@admin.register(Coleta)
class ColetaAdmin(admin.ModelAdmin):
    list_display = ('data', 'temperatura_max', 'temperatura_min',
        'temperatura_media', 'humidade_media', 'velocidade_vento',)
    ordering = ('-data',)
    #list_filter = ('data', 'temperatura_max', 'temperatura_min',
    #    'temperatura_media', 'humidade_media', 'velocidade_vento',)
    #search_fields = ('username', 'first_name',)
