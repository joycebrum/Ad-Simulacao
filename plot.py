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

Espera_X = [0]
Espera_X_Max = 0
Espera_Y = [0]
Espera_Y_Max = 0

Espera_X_Classe = {0: [0], 1: [0]}
Espera_X_Classe_Max = {0: 0, 1: 0}
Espera_Y_Classe = {0: [0], 1: [0]}
Espera_Y_Classe_Max = {0: 0, 1: 0}


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
    
def updateGrafos(filaNP, filaP, servidor, time):
    global Clientes_X, Clientes_Y, Clientes_X_Max, Clientes_Y_Max
    clientesNoSistema = getTotalPessoasNoSistema(filaNP, filaP, servidor)
    Clientes_X.append(time)
    Clientes_X_Max = time
    Clientes_Y.append(clientesNoSistema)
    if clientesNoSistema > Clientes_Y_Max:
        Clientes_Y_Max = clientesNoSistema
    updateGrafoClientesClasse(filaP,servidor,time, 0)
    updateGrafoClientesClasse(filaNP,servidor,time, 1)
    
    updateGrafoEspera(filaNP, filaP, servidor, time)
    
def updateGrafoClientesClasse(fila, servidor, time, priority):
    global Clientes_X_Classe, Clientes_Y_Classe 
    global Clientes_X_Classe_Max, Clientes_Y_Classe_Max
    clientesNoSistema = getTotalPessoasNoSistemaPorClasse(fila, servidor, priority)
    Clientes_X_Classe[priority].append(time)
    Clientes_X_Classe_Max[priority] = time
    Clientes_Y_Classe[priority].append(clientesNoSistema)
    if clientesNoSistema > Clientes_Y_Classe_Max[priority]:
        Clientes_Y_Classe_Max[priority] = clientesNoSistema
        
def updateGrafoEspera(filaNP, filaP, servidor, time):
    global Espera_X, Espera_Y, Espera_X_Max, Espera_Y_Max
    clientesNoSistema = len(filaNP) + len(filaP)
    Espera_X.append(time)
    Espera_X_Max = time
    Espera_Y.append(clientesNoSistema)
    if clientesNoSistema > Clientes_Y_Max:
        Espera_Y_Max = clientesNoSistema
    updateGrafoEsperaClasse(filaP,servidor,time, 0)
    updateGrafoEsperaClasse(filaNP,servidor,time, 1)
    
def updateGrafoEsperaClasse(fila, servidor, time, priority):
    global Espera_X_Classe, Espera_Y_Classe 
    global Espera_X_Classe_Max, Espera_Y_Classe_Max
    clientesNaFila = len(fila)
    Espera_X_Classe[priority].append(time)
    Espera_X_Classe_Max[priority] = time
    Espera_Y_Classe[priority].append(clientesNaFila)
    if clientesNaFila > Espera_Y_Classe_Max[priority]:
        Espera_Y_Classe_Max[priority] = clientesNaFila
        
def getArea(X, Y):
    area = 0
    for i in range(1, len(Clientes_X)):
        dt = X[i] - X[i-1]
        area += (Y[i] - Y[i-1])*dt
    return area


def plotClientesSistema():
    plt.step(Clientes_X, Clientes_Y)
    plt.axis([0, Clientes_X_Max, 0, Clientes_Y_Max])
  
def plotData(xdados, y):
    plt.plot(xdados, y, 'ro')
    plt.axis([0, 450, 0, 100])
    plt.show()
    