# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:18:14 2019

@author: joyce
"""

def calculaTempoMedio(queueTime):
    tempoMedioNaFila = 0
    for tempoi in queueTime :
        tempoMedioNaFila=tempoMedioNaFila+tempoi
    
    if len(queueTime) > 0:
        tempoMedioNaFila = tempoMedioNaFila/len(queueTime)
    else:
        tempoMedioNaFila = 0
    return tempoMedioNaFila