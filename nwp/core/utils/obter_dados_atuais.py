#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil, os
import requests
import pytesseract
from lxml import html, etree
from PIL import Image, ImageEnhance, ImageFilter
import datetime

'''
# Trata a imagem para facilitar o OCR.
im = Image.open('captcha.png') # the second one
im = im.filter(ImageFilter.ModeFilter(1))
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(100)
im = im.convert('1')
im.save('captcha-tratado.png')
text = pytesseract.image_to_string(Image.open('captcha-tratado.png'))
print text
'''

url = 'http://www.inmet.gov.br/sim/sonabra/dspDadosCodigo.php?ODI1OTg='
id = ''
captcha_texto = 0
contador = 0
arvore_dados = None
coletas = {}

while 1:

    contador += 1
    print "[1] Buscando dados..."

    # Obtém página padrão.
    pagina = requests.get(url)
    arvore = html.fromstring(pagina.content)

    print "[2] Obtendo ID da sessão e imagem..."
    # Identifica o id da sessão e figura do captcha.
    id = arvore.xpath("//input[@name='aleaValue']")[0].attrib['value']
    img_src = arvore.xpath("//img")[0].attrib['src']
    img_url = 'http://www.inmet.gov.br/sonabra/' + img_src

    # Faz o download da foto.
    resposta = requests.get(img_url, stream=True)
    with open(os.path.join('temp', 'captcha.png'), 'wb') as arquivo_saida:
        shutil.copyfileobj(resposta.raw, arquivo_saida)
    del resposta

    print "[3] Tentando reconhecer imagem do captcha..."
    # Tenta fazer o OCR da imagem.
    captcha_texto = pytesseract.image_to_string(Image.open(os.path.join('temp', 'captcha.png')))
    try:
        captcha_numero = int(captcha_texto)
    except ValueError:
        print "[3.1] Falhou no reconhecimento. Reinciando processo..."
        print '-----------------------------------------------------------'
        continue

    print "[4] Tentando enviar formulário..."
    session = requests.session()

    ontem = datetime.datetime.now() - datetime.timedelta(days=1)
    anteontem = datetime.datetime.now() - datetime.timedelta(days=2)
    data = {'aleaValue': id, 'dtaini': anteontem.strftime('%d/%m/%Y'), 'dtafim': ontem.strftime('%d/%m/%Y'), 'aleaNum': captcha_texto,}
    pagina = requests.post(url, data=data)

    arvore = html.fromstring(pagina.content)
    # A presença deste botão garante que  captcha passou.
    pagina_ok = arvore.xpath("//input[@name='Submit2']")

    print "[5] Verificando se o envio obteve sucesso..."
    if pagina_ok:
        arvore_dados = arvore
        break
    else:
        print "[5.1] Falhou no envio do formulário. Tentando novamente..."
        print '-----------------------------------------------------------'
        continue

print "[6] Processando tabela com dados."
linhas = arvore_dados.xpath("//table[@border='1']/tbody")[0]

anteontem1 = linhas[0].xpath('./td/span/text()')
anteontem2 = linhas[1].xpath('./td/span/text()')
anteontem3 = linhas[2].xpath('./td/span/text()')

anteontem_data = datetime.datetime.strptime(anteontem1[0], '%d/%m/%Y')
anteontem_humidade_media = float(anteontem1[2])
anteontem_velocidade_vento = float(anteontem1[5])
anteontem_insolacao = float(anteontem1[8])
anteontem_temperatura_max = float(anteontem1[9])
try:
    anteontem_temperatura_min = float(anteontem1[10])
except:
    anteontem_temperatura_min = anteontem_temperatura_max - 3
anteontem_temperatura_media = (anteontem_temperatura_max + anteontem_temperatura_min)/2.0
anteontem_precipitacao = float(anteontem2[10])

coletas[anteontem_data] = {
    'temperatura_min': anteontem_temperatura_min,
    'temperatura_max': anteontem_temperatura_max,
    'temperatura_media': anteontem_temperatura_media,
    'humidade_media': anteontem_humidade_media,
    'insolacao': anteontem_insolacao,
    'velocidade_vento': anteontem_velocidade_vento,
    'precipitacao': anteontem_precipitacao,
}

ontem1 = linhas[3].xpath('./td/span/text()')
ontem2 = linhas[4].xpath('./td/span/text()')
ontem3 = linhas[5].xpath('./td/span/text()')

ontem_data = datetime.datetime.strptime(ontem1[0], '%d/%m/%Y')
ontem_humidade_media = float(ontem1[2])
ontem_velocidade_vento = float(ontem1[5])
ontem_insolacao = float(ontem1[8])
ontem_temperatura_max = float(ontem1[9])
try:
    ontem_temperatura_min = float(ontem1[10])
except:
    ontem_temperatura_min = ontem_temperatura_max - 3
ontem_temperatura_media = (ontem_temperatura_max + ontem_temperatura_min)/2.0
ontem_precipitacao = float(ontem2[8])

coletas[anteontem_data] = {
    'temperatura_min': ontem_temperatura_min,
    'temperatura_max': ontem_temperatura_max,
    'temperatura_media': ontem_temperatura_media,
    'humidade_media': ontem_humidade_media,
    'insolacao': ontem_insolacao,
    'velocidade_vento': ontem_velocidade_vento,
    'precipitacao': ontem_precipitacao,
}


print coletas
