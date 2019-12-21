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

def getTotalPessoasNoSistema(fila1, fila2, servidor):
    if servidor != None:
        return len(fila1) + len(fila2) +1
    else:
        return 0

def updateGrafoClientes(fila1, fila2, servidor, time):
    global Clientes_X, Clientes_Y, Clientes_X_Max, Clientes_Y_Max
    clientesNoSistema = getTotalPessoasNoSistema(fila1, fila2, servidor)
    Clientes_X.append(time)
    Clientes_X_Max = time
    Clientes_Y.append(clientesNoSistema)
    if clientesNoSistema > Clientes_Y_Max:
        Clientes_Y_Max = clientesNoSistema

def getArea():
    area = 0
    for i in range(1, len(Clientes_X)):
        dt = Clientes_X[i] - Clientes_X[i-1]
        area += (Clientes_Y[i] - Clientes_Y[i-1])*dt
    return area

def plotClientesSistema():
    plt.step(Clientes_X, Clientes_Y)
    plt.axis([0, Clientes_X_Max, 0, Clientes_Y_Max])
  
def plotData(xdados, y):
    plt.plot(xdados, y, 'ro')
    plt.axis([0, 450, 0, 100])
    plt.show()
    