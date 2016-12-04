# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-03 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amostra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(unique=True, verbose_name='Data da Coleta')),
                ('temperatura_max', models.FloatField(verbose_name='Temperatura M\xe1xima')),
                ('temperatura_min', models.FloatField(verbose_name='Temperatura M\xednima')),
                ('temperatura_media', models.FloatField(verbose_name='Temperatura M\xe9dia')),
                ('humidade_media', models.FloatField(verbose_name='Humidade M\xe9dia')),
                ('velocidade_vento', models.FloatField(verbose_name='Velocidade do Vento')),
                ('insolacao', models.FloatField(verbose_name='Insola\xe7\xe3o')),
                ('precipitacao', models.FloatField(verbose_name='Precipita\xe7\xe3o')),
            ],
            options={
                'verbose_name': 'Amostra',
                'verbose_name_plural': 'Amostras',
            },
        ),
    ]
