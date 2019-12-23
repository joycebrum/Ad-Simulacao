# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 18:49:31 2019

@author: joyce
"""

BAIXA = 1
ALTA = 0

CHEGADA = "chegada"
SAIDA = "saida"

def cenarios1():
    return geraLambda1(0, 1, 0.5, True)

def cenarios2():
    return geraLambda1(0.2, 1, 0.5, False)

## ver essa parte ##
def cenarios3():
    return geraLambda1(0.2, 1, 0.5, False)

def cenarios4():
    return geraLambda1(0.05, 1, 0.5, False)
## ver aqui em cima ##

def geraLambda1(lambda2, mi1, mi2, is1):
    la = 0.05
    cenarios = []
    if(is1):
        for i in range (0, 18):
            cenarios.append([round(la + la*i, 2), lambda2, mi1, mi2])
    else:
        for i in range (0, 12):
            cenarios.append([round(la + la*i, 2), lambda2, mi1, mi2])
    return cenarios
        