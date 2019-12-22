# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:18:14 2019

@author: joyce
"""
import plot
import numpy as np
from variables import ALTA
from variables import BAIXA

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
        print(la1, mi1)
        return la1 / mi1

def Ro_Geral(comClasse):
    if comClasse:
        return la1/mi1 + la2/mi2
    else:
        return la1/mi1


def printTabelaFilaUnica(actualTime, totalClientes, ro):
    teams_list = ["E[N]", "E[T]", "E[Nq]", "E[W]"]
    data = np.array([[round( numeroMedio(actualTime, plot.Clientes_X, plot.Clientes_Y), 2), 
                      round( tempoMedio(totalClientes[1], plot.Clientes_X, plot.Clientes_Y), 2),
                      round( numeroMedio(actualTime, plot.Espera_X, plot.Espera_Y), 2), 
                      round( tempoMedio(totalClientes[1], plot.Espera_X, plot.Espera_Y), 2)
                    ]])
    printTabela(teams_list, data)
    
    teams_list = ["E[Xr]"]
    data = np.array([[round(tempoMedio(totalClientes[1], plot.Trabalho_Residual_X, plot.Trabalho_Residual_Y), 2)]])
    printTabela(teams_list,data)
    


def getUAnalitico_NPreemptive():
    p1 = Ro_Analitico(ALTA)
    p2 = Ro_Analitico(BAIXA)
    p = Ro_Geral(True)
    W1_Analitico = pXr/(1-p1)
    W2_Analitico = (p1*W1_Analitico + pXr)/(1-p)
    return p1*W1_Analitico + p2*W2_Analitico + pXr

def getUAnalitico_Preemptive():
    p1 = Ro_Analitico(ALTA)
    p2 = Ro_Analitico(BAIXA)
    p = Ro_Geral(True)
    W1_Analitico = p1/(mi1*(1-p1))
    W2_Analitico = (p1*W1_Analitico + pXr + p1/mi2)/(1-p)
    return p1*W1_Analitico + p2*W2_Analitico + pXr

def printTabelaFilaClasse(actualTime, totalClientes, la1t, la2t, mi1t, mi2t, preemptive):
    global la1, la2, mi1, mi2, pXr
    la1 = la1t
    la2 = la2t
    mi1 = mi1t
    mi2 = mi2t
    pXr = Ro_Analitico(ALTA)*1/mi1 + Ro_Analitico(BAIXA)*1/mi2
    
    if preemptive:
        U_Analitico = getUAnalitico_Preemptive()
    else:
        U_Analitico = getUAnalitico_NPreemptive()
    U = Nq(actualTime, ALTA)*1/mi1 + Nq(actualTime, BAIXA)*1/mi2 + pXr
    teams_list = ["E[U](2)", "E[U](3)", "E[Nq1]", "E[Nq2]", "E[U](4)"]
    data = np.array([[round(pXr/(1 - Ro_Geral(True)), 2),
                      round(U_Analitico, 2),
                      round(Nq(actualTime, ALTA), 2), 
                      round(Nq(actualTime, BAIXA), 2),
                      round(U, 2)
                    ]])
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

