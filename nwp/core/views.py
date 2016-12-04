# -*- coding: utf-8 -*-

import os, csv, datetime, random, numpy
from django.shortcuts import render
from django.views.generic import View

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
