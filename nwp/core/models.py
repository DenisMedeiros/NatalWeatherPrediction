# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Coleta(models.Model):
    data = models.DateField(unique=True,
        verbose_name='Data da Coleta')
    temperatura_max = models.FloatField(blank=False, null=False,
        verbose_name='Temperatura Máxima')
    temperatura_min = models.FloatField(blank=False, null=False,
        verbose_name='Temperatura Mínima')
    temperatura_media = models.FloatField(blank=False, null=False,
        verbose_name='Temperatura Média')
    humidade_media = models.FloatField(blank=False, null=False,
        verbose_name='Humidade Média')
    velocidade_vento = models.FloatField(blank=False, null=False,
        verbose_name='Velocidade do Vento')
    insolacao = models.FloatField(blank=False, null=False,
        verbose_name='Insolação')
    precipitacao = models.FloatField(blank=False, null=False,
        verbose_name='Precipitação')

    def __unicode__(self):
        return 'Coleta #%d' %self.id

    class Meta:
        verbose_name = u'Coleta'
        verbose_name_plural = u'Coletas'
