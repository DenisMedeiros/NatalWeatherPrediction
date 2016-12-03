# -*- coding: utf-8 -*-
from core.models import Amostra
import os, csv

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'resource', 'dados_inmet.csv')

def csv2db():
    with open(file_path, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            print row
