# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:18:14 2019

@author: joyce
"""
import plot
import numpy as np
from variables import ALTA
from variables import BAIXA
import intervaloDeConfianca as ic


la1 = 0
la2 = 0
mi1 = 0
mi2 = 0
pXr = 0

def updateTempoEspera(queue, step):
    for element in queue:
        element.clientData.esperaFila += step
        
def updateTempoExecutando(queue, step):
    for element in queue:
        element.clientData.executando += step

def tempoMedio(numeroClientes, X, Y):
    if numeroClientes == 0:
        return 0
    return plot.getArea(X, Y)/numeroClientes

def numeroMedio(tempoTotal, X, Y):
    #TODO not implemented yet
    return plot.getArea(X, Y)/tempoTotal

def Xr(totalClientes, classe):
    return tempoMedio(totalClientes[classe], plot.Trabalho_Residual_X_Classe[classe], plot.Trabalho_Residual_Y_Classe[classe])

def Nq(actualTime, classe):
    return numeroMedio(actualTime,plot.Espera_X_Classe[classe], plot.Espera_Y_Classe[classe])

def Nq_filaUnica(actualTime):
    return numeroMedio(actualTime,plot.Espera_X, plot.Espera_Y)

def NqAnalitico(la1,la2, mi1, mi2, isFilaUnica):
    if isFilaUnica:
        p1 = la1/mi1
        p2 = la2/mi2
        w = (p1/mi1+p2/mi2) / (1-p1-p2)
        nq1 = la1 * w
        nq2 = la2 * w
        return nq1 + nq2
    return ( ( pow(la,2)/pow(mi,2) ) / ( 1-(la/mi) ) )

def W(totalClientes, classe):
    return tempoMedio(totalClientes[classe],plot.Espera_X_Classe[classe], plot.Espera_Y_Classe[classe])

def N(actualTime, classe):
    return numeroMedio(actualTime,plot.Clientes_X_Classe[classe], plot.Clientes_Y_Classe[classe]) 

def T(totalClientes, classe):
    return tempoMedio(totalClientes[classe],plot.Clientes_X_Classe[classe], plot.Clientes_Y_Classe[classe])

def Ro_Analitico(classe):
    if classe == BAIXA:
        return la2 / mi2
    else:
        return la1 / mi1

def Ro_Geral(comClasse):
    print("a", la1, mi1, la2, mi2)
    if comClasse:
        return la1/mi1 + la2/mi2
    else:
        return la2/mi2

def getUAnalitico_NPreemptive():
    p1 = Ro_Analitico(ALTA)
    p2 = Ro_Analitico(BAIXA)
    p = Ro_Geral(True)
    W1_Analitico = pXr/(1-p1)
    print("p = ", p)
    W2_Analitico = (p1*W1_Analitico + pXr)/(1-p)
    return p1*W1_Analitico + p2*W2_Analitico + pXr

def getUAnalitico_Preemptive():
    p1 = Ro_Analitico(ALTA)
    p2 = Ro_Analitico(BAIXA)
    p = Ro_Geral(True)
    W1_Analitico = p1/(mi1*(1-p1))
    W2_Analitico = (p1*W1_Analitico + pXr + p1/mi2)/(1-p)
    return p1*W1_Analitico + p2*W2_Analitico + pXr

def getUAnalitico_Unica():
    p =  Ro_Geral(False)
    W = p/(mi2 * (1-p))
    return p*W + pXr

def getMediaAmostralFila():
    Nq1 = ic.mediaAmostral(plot.Espera_Y_Classe[ALTA])
    Nq2 = ic.mediaAmostral(plot.Espera_Y_Classe[BAIXA])
    return [round(Nq1,3), round(Nq2,3)]

def printTabelaFilaClasse(actualTime, totalClientes, la1t, la2t, mi1t, mi2t, preemptive, isFilaUnica):
    global la1, la2, mi1, mi2, pXr
    la1 = la1t
    la2 = la2t
    mi1 = mi1t
    mi2 = mi2t
    pXr = Ro_Analitico(ALTA)*1/mi1 + Ro_Analitico(BAIXA)*1/mi2
    if isFilaUnica:
        p =  Ro_Geral(not isFilaUnica)
        pXr = p*1/mi2
        U_Analitico = getUAnalitico_Unica()
    elif preemptive:
        U_Analitico = getUAnalitico_Preemptive()
    else:
        U_Analitico = getUAnalitico_NPreemptive()
    U = Nq(actualTime, ALTA)*1/mi1 + Nq(actualTime, BAIXA)*1/mi2 + pXr
    teams_list = ["E[U](2)", "E[U](3)", "E[Nq1]", "E[Nq2]", "E[U](4)"]
    data = np.array([[round(pXr/(1 - Ro_Geral(not isFilaUnica)), 2),
                      round(U_Analitico, 2),
                      round(Nq(actualTime, ALTA), 2), 
                      round(Nq(actualTime, BAIXA), 2),
                      round(U, 2)
                    ]])
    printTabela(teams_list, data)
    
    printMediaAmostralFila()

def printMediaAmostralFila():
    teams_list = ["Média Nq1", "Média Nq2"]
    data = np.array([getMediaAmostralFila()])
    printTabela(teams_list, data)

def printTabela(teams_list, data):
    row_format ="{:>15}" * (len(teams_list) + 1)
    print(row_format.format("", *teams_list))
    for team, row in zip(teams_list, data):
        print(row_format.format("", *row))
    
    print("\n")

def getDataClasse(actualTime, totalClientes, X, Y):
     return np.array([[round(numeroMedio(actualTime,X[0], Y[0]), 2), 
                      round(tempoMedio(totalClientes[0], X[0], Y[0]),2),
                      round(numeroMedio(actualTime,X[1], Y[1]), 2), 
                      round(tempoMedio(totalClientes[1],X[1], Y[1]),2)
                    ]])

