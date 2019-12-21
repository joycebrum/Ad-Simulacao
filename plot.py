# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 20:54:19 2019

@author: joyce
"""

import matplotlib.pyplot as plt

Clientes_X = [0]
Clientes_X_Max = 0
Clientes_Y = [0]
Clientes_Y_Max = 0

Clientes_X_Classe = {0: [0], 1: [0]}
Clientes_X_Classe_Max = {0: 0, 1: 0}
Clientes_Y_Classe = {0: [0], 1: [0]}
Clientes_Y_Classe_Max = {0: 0, 1: 0}


def getTotalPessoasNoSistema(fila1, fila2, servidor):
    if servidor != None:
        return len(fila1) + len(fila2) +1
    else:
        return 0

def getTotalPessoasNoSistemaPorClasse(fila, servidor, priority):
    if servidor != None:
        if servidor.priority == priority:
            return len(fila) + 1
        return len(fila)
    else:
        return 0
    
def updateGrafoClientes(filaNP, filaP, servidor, time):
    global Clientes_X, Clientes_Y, Clientes_X_Max, Clientes_Y_Max
    clientesNoSistema = getTotalPessoasNoSistema(filaNP, filaP, servidor)
    Clientes_X.append(time)
    Clientes_X_Max = time
    Clientes_Y.append(clientesNoSistema)
    if clientesNoSistema > Clientes_Y_Max:
        Clientes_Y_Max = clientesNoSistema
    updateGrafoClientesClasse(filaP,servidor,time, 0)
    updateGrafoClientesClasse(filaNP,servidor,time, 1)
    
def updateGrafoClientesClasse(fila, servidor, time, priority):
    global Clientes_X_Classe, Clientes_Y_Classe 
    global Clientes_X_Classe_Max, Clientes_Y_Classe_Max
    clientesNoSistema = getTotalPessoasNoSistemaPorClasse(fila, servidor, priority)
    Clientes_X_Classe[priority].append(time)
    Clientes_X_Classe_Max[priority] = time
    Clientes_Y_Classe[priority].append(clientesNoSistema)
    if clientesNoSistema > Clientes_Y_Classe_Max[priority]:
        Clientes_Y_Classe_Max[priority] = clientesNoSistema
        
def getArea():
    area = 0
    for i in range(1, len(Clientes_X)):
        dt = Clientes_X[i] - Clientes_X[i-1]
        area += (Clientes_Y[i] - Clientes_Y[i-1])*dt
    return area

def getAreaPorClasse(priority):
    area = 0
    for i in range(1, len(Clientes_X_Classe[priority])):
        dt = Clientes_X_Classe[priority][i] - Clientes_X_Classe[priority][i-1]
        area += (Clientes_Y_Classe[priority][i] - Clientes_Y_Classe[priority][i-1])*dt
    return area


def plotClientesSistema():
    plt.step(Clientes_X, Clientes_Y)
    plt.axis([0, Clientes_X_Max, 0, Clientes_Y_Max])
  
def plotData(xdados, y):
    plt.plot(xdados, y, 'ro')
    plt.axis([0, 450, 0, 100])
    plt.show()
    