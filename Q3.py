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
from intervaloDeConfianca import calculaIntervaloDeConfianca
import variables as variables
import calculosMedia as cm
import plot as pl

tamanho = 121

def Q3_B():
    ## LETRA B ##
    #executaCenario1(True, False)
    #executaCenario2(True, False)
    #executaCenario3(True, False)
    executaCenario4(True, False)

def Q3_A():
    ## LETRA A ##
    #executaCenario1(True, True)
    #executaCenario2(True, True)
    #executaCenario3(True, True)
    executaCenario4(True, True)
    
def Q4_B():
    ## LETRA B ##
    #executaCenario1(False, False)
    #executaCenario2(False, False)
    #executaCenario3(False, False)
    executaCenario4(False, False)

def Q4_A():
    ## LETRA A ##
    #executaCenario1(False, True)
    #executaCenario2(False, True)
    #executaCenario3(False, True)
    executaCenario4(False, True)


def executaCenario1(isQ3, isA):
    if(isA):
        executaCenarioA(variables.cenarios1(), isQ3, 0.9, 'e')
    else:
        executaCenarioB(variables.cenarios1(), isQ3, 0.9, 'e')

def executaCenario2(isQ3, isA):
    if(isA):
        executaCenarioA(variables.cenarios2(), isQ3, 0.6, 'e')
    else:
        executaCenarioB(variables.cenarios2(), isQ3, 0.6, 'e')

def executaCenario3(isQ3, isA):
    if(isA):
        executaCenarioA(variables.cenarios3(), isQ3, 0.6, 'd')
    else:
        executaCenarioB(variables.cenarios3(), isQ3, 0.6, 'd')

def executaCenario4(isQ3, isA):
    if(isA):
        executaCenarioA(variables.cenarios4(), isQ3, 0.1, 'u' )
    else:
        executaCenarioB(variables.cenarios4(), isQ3, 0.1, 'u' )

def executaCenarioA(cenarios, isFilaUnica, maxLambda, tipoDeFila):
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
            tempo = filaUnica()[0]
            pessoas = cm.Nq_filaUnica(tempo)
            print("para lambda1 = ", la1, " intervalo de confiança de +/-", round(calculaIntervaloDeConfianca(pl.Espera_Y),2))
       
        else:
            tempo = filaDuplaSemPreempcao()[0]
            pessoas = cm.Nq(tempo, variables.ALTA) + cm.Nq(tempo, variables.BAIXA)
            print("para lambda1 = ", la1, " intervalo de confiança de +/-", round(calculaIntervaloDeConfianca(pl.Espera_Y_Classe[variables.ALTA]),2), "para a classe 1 e de +-", round(calculaIntervaloDeConfianca(pl.Espera_Y_Classe[variables.BAIXA]),2), " para a classe 2")
            
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
    
def executaCenarioB(cenarios, isFilaUnica, maxLambda, tipoDeFila):
    vetorDePlotagemX = []
    vetorDePlotagemY1 = []
    vetorDePlotagemX2 = []
    vetorDePlotagemY2 = []
    
    maxTempo = 0
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho, tipoDeFila)
        la1 = cenario[0]
        la2 = cenario[1]
        mi1 = cenario[2]
        mi2 = cenario[3]
        
        vetorDePlotagemX.append(cenario[0]-0.025)
        vetorDePlotagemX.append(cenario[0]-0.025)
        vetorDePlotagemX.append(cenario[0]+0.025)
        vetorDePlotagemX.append(cenario[0]+0.025)
        
        if isFilaUnica:
            vetorTimePessoas = filaUnica()
            totalPessoas = vetorTimePessoas[1]
            tempo = cm.W_filaUnica(totalPessoas)
            distribuicaoTempoDeEspera = cm.tempoEspera_FilaUnica(vetorTimePessoas[1], vetorTimePessoas[0])
            print("para lambda1 = ", la1, " intervalo de confiança de +/-", round(calculaIntervaloDeConfianca(distribuicaoTempoDeEspera),2))
            
            vetorDePlotagemY1.append(0)
            vetorDePlotagemY1.append(tempo)
            vetorDePlotagemY1.append(tempo)
            vetorDePlotagemY1.append(0)
            
        else:
            vetorTimePessoas = filaDuplaSemPreempcao()
            totalPessoas = vetorTimePessoas[1]
            tempo1 = cm.W(totalPessoas, variables.ALTA)
            tempo2 = cm.W(totalPessoas, variables.BAIXA)
            tempo = cm.getWGeral(tempo1, tempo2, la1, la2)
            distribuicaoTempoDeEspera1 = cm.tempoEspera(vetorTimePessoas[1], vetorTimePessoas[0], variables.ALTA)
            distribuicaoTempoDeEspera2 = cm.tempoEspera(vetorTimePessoas[1], vetorTimePessoas[0], variables.BAIXA)
            print("para lambda1 = ", la1, " intervalo de confiança de +/-", round(calculaIntervaloDeConfianca(distribuicaoTempoDeEspera1),2), "para a classe 1 e de +-", round(calculaIntervaloDeConfianca(distribuicaoTempoDeEspera2),2), " para a classe 2")
            vetorDePlotagemY1.append(0)
            vetorDePlotagemY1.append(tempo)
            vetorDePlotagemY1.append(tempo)
            vetorDePlotagemY1.append(0)
        
        if maxTempo < tempo:
            maxTempo = tempo
        
        if tipoDeFila == 'e':
            tempoSeparadoPorClasse = cm.WAnaliticoExp(la1, la2, mi1, mi2, isFilaUnica)
        elif tipoDeFila == 'd':
            tempoSeparadoPorClasse = cm.WAnaliticoDeter(la1, la2, mi1, mi2, isFilaUnica)
        elif tipoDeFila == 'u':
            tempoSeparadoPorClasse = cm.WAnaliticoUni(la1, la2, mi1, mi2, isFilaUnica)
        tempoAnalitico = tempoSeparadoPorClasse[0] + tempoSeparadoPorClasse[1]
        if tempoAnalitico >= 0:
            if maxTempo < tempoAnalitico:
                maxTempo = tempoAnalitico
                
            vetorDePlotagemX2.append(la1)
            vetorDePlotagemY2.append(tempoAnalitico)
            
    plotFunction(vetorDePlotagemX, vetorDePlotagemY1, maxLambda + 0.05 , maxTempo+0.5)
    #plotFunction(vetorDePlotagemX, vetorDePlotagemY2, maxLambda + 0.05 , maxTempo+0.5)
    if tipoDeFila == 'u':
        plotData(vetorDePlotagemX2, vetorDePlotagemY2, maxLambda + 0.05,  maxTempo+0.5)    
    else:
        plotFunction(vetorDePlotagemX2, vetorDePlotagemY2, maxLambda + 0.05,  maxTempo+0.5)
    


def main():
    #Q3()
    Q3_A()

        

main()

    
