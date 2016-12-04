# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-03 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amostra',
            name='humidade_media',
            field=models.FloatField(verbose_name='Humidade M\xe9dia'),
        ),
        migrations.AlterField(
            model_name='amostra',
            name='momento_coleta',
            field=models.DateField(unique=True, verbose_name='Momento da Coleta'),
        ),
        migrations.AlterField(
            model_name='amostra',
            name='temperatura_max',
            field=models.FloatField(verbose_name='Temperatura M\xe1xima'),
        ),
        migrations.AlterField(
            model_name='amostra',
            name='temperatura_media',
            field=models.FloatField(verbose_name='Temperatura M\xe9dia'),
        ),
        migrations.AlterField(
            model_name='amostra',
            name='temperatura_min',
            field=models.FloatField(verbose_name='Temperatura M\xednima'),
        ),
        migrations.AlterField(
            model_name='amostra',
            name='velocidade_vento',
            field=models.FloatField(verbose_name='Velocidade do Vento'),
        ),
    ]
