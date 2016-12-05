#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html

url = 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?QTMwNA=='

# Obtém página padrão.
page = requests.get(url)
tree = html.fromstring(page.content)

captcha = tree.xpath("//input[@name='aleaValue']")

print captcha[0]

exit()

headers = {'content-type': 'application/json'}

data = {"eventType": "AAS_PORTAL_START", "data": {"uid": "hfe3hf45huf33545", "aid": "1", "vid": "1"}}
params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}

response = requests.post(url, params=params, data=params, headers=headers)