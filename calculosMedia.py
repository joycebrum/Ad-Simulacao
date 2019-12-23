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

def NqAnaliticoExp(la1,la2, mi1, mi2, isFilaUnica):
    p1 = la1/mi1
    p2 = la2/mi2
    ## Questão 3 - cenario 1 e 2 ##
    if not (la1 == 0.6 and la2 == 0.2):
        if isFilaUnica:
            w = (p1/mi1+p2/mi2) / (1-p1-p2)
            nq1 = la1 * w
            nq2 = la2 * w
            return [nq1, nq2]
        ## Questão 4 - cenario 1 e 2 ##
        else: #sem preempção
            pXr = p1/mi1 + p2/mi2
            w1 = pXr/(1-p1)
            nq1 = la1*w1
            w2 = (p1*w1 + pXr)/(1-p1-p2)
            nq2 = la2*w2
            return [nq1, nq2]
    else:
        return [-1,0]
def NqAnaliticoDeter(la1,la2, mi1, mi2, isFilaUnica):
    p1 = la1/mi1
    p2 = la2/mi2
    ## Questão 3 - cenario 3 ##
    if not la1 == 0.6 and la2 == 0.2:
        if isFilaUnica:
            w = (p1/(2*mi1) + p2/(2*mi2)) / (1-p1-p2)
            nq1 = la1 * w
            nq2 = la2 * w
            return [nq1, nq2]
        ## Questão 4 - cenario 3 ##
        else:
            print("TODO")
    else:
        return [-1, 0]
    
def NqAnaliticoUni(la1,la2, mi1, mi2, isFilaUnica):
    a1 = mi1[0]
    a2 = mi2[0]
    b1 = mi1[1]
    b2 = mi2[1]
    p1 = la1*(a1+b1)/2
    p2 = la2*(a2+b2)/2
    ## Questão 3 - cenario 4 ##
    if isFilaUnica:
        w1 = (p1*(pow(a1,2) + a1*b1 + pow(b1,2)))/(3*(a1+b1))
        w2 = (p2*(pow(a2,2) + a2*b2 + pow(b2,2)))/(3*(a2+b2))
        w = (w1 + w2)/(1-p1-p2)
        nq1 = la1 * w
        nq2 = la2 * w
        return [nq1, nq2]
     ## Questão 4 - cenario 4 ##
    else:
        print("TODO")
        
        
def W(totalClientes, classe):
    return tempoMedio(totalClientes[classe],plot.Espera_X_Classe[classe], plot.Espera_Y_Classe[classe])

def W_filaUnica(totalClientes):
    return tempoMedio(totalClientes[0] + totalClientes[1],plot.Espera_X, plot.Espera_Y)

def tempoEspera_FilaUnica(totalClientes, actualTime):
    w = []
    tot = totalClientes[0] + totalClientes[1]
    for nq in plot.Espera_Y:
        w.append((actualTime/tot) * nq)
    return w

def tempoEspera(totalClientes, actualTime, classe):
    w = []
    tot = totalClientes[0] + totalClientes[1]
    for nq in plot.Espera_Y_Classe[classe]:
        w.append((actualTime/tot) * nq)
    return w

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
    if p == 1:
        return 99999
    W2_Analitico = (p1*W1_Analitico + pXr)/(1-p)
    return p1*W1_Analitico + p2*W2_Analitico + pXr

def getUAnalitico_Preemptive():
    p1 = Ro_Analitico(ALTA)
    p2 = Ro_Analitico(BAIXA)
    p = Ro_Geral(True)
    if p == 1:
        return 99999
    W1_Analitico = p1/(mi1*(1-p1))
    W2_Analitico = (p1*W1_Analitico + pXr + p1/mi2)/(1-p)
    return p1*W1_Analitico + p2*W2_Analitico + pXr

def getUAnalitico_Unica(la1, la2, mi1, mi2):
    p1 = la1/mi1
    p2 = la2/mi2
    if p1 + p2 == 1:
        return 99999
    pXr = p1/mi1 + p2/mi2
    W = pXr/(1-p1-p2)
    print("nq=", NqAnalitico(la1, la2, mi1, mi2, True), "w=",W)
    return NqAnalitico(la1, la2, mi1, mi2, True)/(mi1+mi2) + pXr

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
    p1 = la1/mi1
    p2 = la2/mi2
    pXr = p1/mi1 + p2/mi2
    if isFilaUnica:
        p =  Ro_Geral(not isFilaUnica)
        pXr = p*1/mi2
        U_Analitico = getUAnalitico_Unica(la1, la2, mi1, mi2)
    elif preemptive:
        U_Analitico = getUAnalitico_Preemptive()
    else:
        U_Analitico = getUAnalitico_NPreemptive()
    U = Nq(actualTime, ALTA)*1/mi1 + Nq(actualTime, BAIXA)*1/mi2 + pXr
    teams_list = ["E[U](2)", "E[U](3)", "E[Nq1]", "E[Nq2]", "E[U](4)"]
    if Ro_Geral(not isFilaUnica) == 1:
        U_Analitico_2 = 99999
    elif isFilaUnica:
        U_Analitico_2 = pXr/(1 - p1 - p2)
    else:
        U_Analitico_2 = pXr/(1 - p1 - p2)
    data = np.array([[round(U_Analitico_2, 2),
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

