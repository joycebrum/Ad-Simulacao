# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:19:24 2019

@author: Thiago
"""
from simulador import filaDuplaSemPreempcao
from simulador import filaUnica
from simulador import inicializaGlobalVariables
from plot import plotFunction
from plot import plotData
import variables as variables
import calculosMedia as cm

tamanho = 121

def Q3():
    #executaCenario1(True)
    #executaCenario2(True)
    #executaCenario3(True)
    executaCenario4(True)

def Q4():
    #executaCenario1(False)
    executaCenario2(False)
    #executaCenario3(False)


def executaCenario1(isQ3):
    executaCenario(variables.cenarios1(), isQ3, 0.9, 'e')

def executaCenario2(isQ3):
    executaCenario(variables.cenarios2(), isQ3, 0.6, 'e')

def executaCenario3(isQ3):
    executaCenario(variables.cenarios3(), isQ3, 0.6, 'd')

def executaCenario4(isQ3):
    executaCenario(variables.cenarios4(), isQ3, 0.1, 'u' )

def executaCenario(cenarios, isFilaUnica, maxLambda, tipoDeFila):
    vetorDePlotagemX = []
    vetorDePlotagemY = []
    vetorDePlotagemX2 = []
    vetorDePlotagemY2 = []
    maxPessoas = 0
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho, tipoDeFila)
        la1 = cenario[0]
        la2 = cenario[1]
        mi1 = cenario[2]
        mi2 = cenario[3]
        if isFilaUnica:
            tempo = filaUnica()
            pessoas = cm.Nq_filaUnica(tempo)
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
        
        if tipoDeFila == 'e':
            pessoasSeparadoPorClasse = cm.NqAnaliticoExp(la1, la2, mi1, mi2, isFilaUnica)
        elif tipoDeFila == 'd':
            pessoasSeparadoPorClasse = cm.NqAnaliticoDeter(la1, la2, mi1, mi2, isFilaUnica)
        elif tipoDeFila == 'u':
            pessoasSeparadoPorClasse = cm.NqAnaliticoUni(la1, la2, mi1, mi2, isFilaUnica)
        pessoas = pessoasSeparadoPorClasse[0] + pessoasSeparadoPorClasse[1]
        if pessoas >= 0:
            if maxPessoas < pessoas:
                maxPessoas = pessoas
                
            vetorDePlotagemX2.append(cenario[0])
            vetorDePlotagemY2.append(pessoas)
        
    plotFunction(vetorDePlotagemX, vetorDePlotagemY, maxLambda + 0.05 , maxPessoas+0.5)
    if tipoDeFila == 'u':
        plotData(vetorDePlotagemX2, vetorDePlotagemY2, maxLambda + 0.05,  maxPessoas+0.5)    
    else:
        plotFunction(vetorDePlotagemX2, vetorDePlotagemY2, maxLambda + 0.05,  maxPessoas+0.5)
    


def main():
    #Q3()
    Q4()

        

main()

    
