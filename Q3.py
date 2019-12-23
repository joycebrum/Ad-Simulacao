# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:19:24 2019

@author: Thiago
"""
from simulador import filaDuplaSemPreempcao
from simulador import filaUnica
from simulador import inicializaGlobalVariables
from plot import plotFunction
import variables as variables
import calculosMedia as cm

tamanho = 100

def executaCenario1():
    executaCenarioExp(variables.cenarios1(), True)

def executaCenario2():
    executaCenarioExp(variables.cenarios2(), True)

def executaCenarioExp(cenarios, isFilaUnica):
    vetorDePlotagemX = []
    vetorDePlotagemY = []
    vetorDePlotagemX2 = []
    vetorDePlotagemY2 = []
    maxPessoas = 0
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho)
        la = cenario[0] + cenario[1]
        mi = cenario[2] + cenario[3]
        if isFilaUnica:
            tempo = filaUnica()
        else:
            tempo = filaDuplaSemPreempcao()
        pessoas = cm.Nq(tempo, variables.ALTA) + cm.Nq(tempo, variables.BAIXA)
        if maxPessoas < pessoas:
            maxPessoas = pessoas
        
        vetorDePlotagemX.append(cenario[0]-0.025)
        vetorDePlotagemX.append(cenario[0]-0.025)
        vetorDePlotagemX.append(cenario[0]+0.025)
        vetorDePlotagemX.append(cenario[0]+0.025)
        
        vetorDePlotagemY.append(0)
        vetorDePlotagemY.append(pessoas)
        vetorDePlotagemY.append(pessoas)
        vetorDePlotagemY.append(0)
        
        pessoas = cm.NqAnalitico(la, mi)
        if maxPessoas < pessoas:
            maxPessoas = pessoas
            
        vetorDePlotagemX2.append(cenario[0])
        vetorDePlotagemY2.append(pessoas)
        
        
        
    plotFunction(vetorDePlotagemX, vetorDePlotagemY, 0.95, maxPessoas+0.1)
    plotFunction(vetorDePlotagemX2, vetorDePlotagemY2, 0.95, maxPessoas+0.1)
    


def main():
    #executaCenario1()
    executaCenario2()
    #filaDuplaComPreempcao(la1, la2, mi1, mi2)
    #filaDuplaSemPreempcao(la1, la2, mi1, mi2)

        

main()

    