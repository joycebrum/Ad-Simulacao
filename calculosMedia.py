# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:18:14 2019

@author: joyce
"""
import plot
import numpy as np
from variables import ALTA
from variables import BAIXA

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
    

def printTabelaFilaClasse(actualTime, totalClientes, ro):
    teams_list = ["E[N1]", "E[T1]","E[N2]", "E[T2]"]
    data = getDataClasse(actualTime, totalClientes, plot.Clientes_X_Classe, plot.Clientes_Y_Classe)
    printTabela(teams_list, data)
    
    teams_list = ["E[Nq1]", "E[W1]","E[Nq2]", "E[W2]"]
    data = getDataClasse(actualTime, totalClientes, plot.Espera_X_Classe, plot.Espera_Y_Classe)
    printTabela(teams_list, data)
    
    teams_list = ["E[Xr1]", "E[Xr2]"]
    data = np.array([[round(Xr(totalClientes, ALTA),2),
                      round(Xr(totalClientes, BAIXA),2)
                    ]])
    printTabela(teams_list, data)
    
    pXr = ro[BAIXA]*Xr(totalClientes,BAIXA) + ro[ALTA]*Xr(totalClientes, ALTA)
    ros = ro[BAIXA] + ro[ALTA]
    teams_list = ["E[U](2)", "E[U](3)", "E[Nq1]", "E[Nq2]", "E[U](4)"]
    data = np.array([[round(pXr/(1-ros), 2), 0, 
                      round(Nq(actualTime, ALTA), 2), 
                      round(Nq(actualTime, BAIXA), 2), 0
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

