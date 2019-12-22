# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 18:49:31 2019

@author: joyce
"""

BAIXA = 1
ALTA = 0

CHEGADA = "chegada"
SAIDA = "saida"

def cenarios2():
    la = 0.05
    cenarios = []
    for i in range (0, 12):
       cenarios.append([round(la + la*i, 2), 0.2, 1, 0.5])
    return cenarios