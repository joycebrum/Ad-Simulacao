# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 21:24:57 2019

@author: joyce
"""

from numpy.random import exponential
from collections import namedtuple

from LinkedList import SLinkedList
import calculosMedia
import queue
import random
import plot

from variables import BAIXA
from variables import ALTA

la1 = 0
mi1 = 0
la2 = 0
mi2 = 0
depuracao = False

todosClientes = []
Evento = namedtuple("Evento", "time event priority")

tempoOcupado = [0,0] 
class ClientData :
    def __init__(self, priority = 1, arrivalTime=-1, service = -1):
        self.priority = priority 
        self.arrivalTime = arrivalTime
        self.executed = 0 
        self.service = service
        self.esperaFila = 0
        self.executando = 0
    def getTimeRemaining(self):
        time = self.service - self.executed
        if abs(time) < 0.000000001:
            return 0
        return time
    def console(self):
        print("prioridade: ", self.priority, " arrivalTime: ", round(self.arrivalTime,2), " timeRemaining: ", round(self.getTimeRemaining(),2))

Client = namedtuple("Client", "priority id clientData")
actualTime = 0
previousTime = -1

isFilaUnica = True
preemptive = False

eventos = SLinkedList()
clientesPrio = queue.Queue()
clientesNPrio = queue.Queue()
clientesFilaUnica = queue.Queue()

globalId = 0

queueTime = {}
servidor = None
n_amostras = 0

totalClientes = [0, 0]
tamanho = 10

def nextArrival(la):
    return exponential(1/la)

def nextService(mi):
    return exponential(1/mi)

def chegada(arrivedEvent):
    global actualTime
    global globalId, n_amostras
    n_amostras += 1
    if n_amostras < tamanho:
        if random.random() <= la1/(la1+la2):
            updateNextArrival(ALTA, la1)
        else:
            updateNextArrival(BAIXA, la2)
    clientData = ClientData(arrivedEvent.priority, actualTime, -1)
    cliente = Client(arrivedEvent.priority, globalId, clientData)
    if depuracao:
        printCliente(cliente, "chegou")
    todosClientes.append(cliente)
    globalId+=1
    checkServer(cliente)
    
    
def updateNextArrival(priority, la):
    global totalClientes
    nextA = nextArrival(la)
    proximaChegada = Evento(actualTime + nextA, "chegada", priority)
    eventos.add(proximaChegada)
    totalClientes[priority] += 1
    
def updateNextExit(tempoExecucao, nextClient):
    interruption = eventos.getInterruption(actualTime + tempoExecucao, nextClient.priority)
    if isFilaUnica or interruption == None or not preemptive: #so adiciona evento de saida se nao for ser interrompido
        return eventos.add(Evento(actualTime + tempoExecucao, "saida", nextClient.priority))

def saida(exitEvent, mi):
    global servidor
    if depuracao:
        printCliente(servidor, "saiu")
    
    if isFilaUnica:
        if not clientesFilaUnica.empty():
            nextClient = clientesFilaUnica.get()
            serverClient(nextClient)
        else:
            servidor = None
    elif not clientesPrio.empty() :
        nextClient = clientesPrio.get()
        serverClient(nextClient)
    else:
        if not clientesNPrio.empty():
            nextClient = clientesNPrio.get()
            serverClient(nextClient)
        else:
            servidor = None
    
def checkServer(cliente):
    global servidor
    global clientesPrio
    global clientesNPrio
    if servidor == None:
        serverClient(cliente)
    elif preemptive and cliente.priority < servidor.priority:
        interrupt(cliente)
    else:
        if isFilaUnica:
            clientesFilaUnica.put(Client(cliente.priority, cliente.id, cliente.clientData))
        elif cliente.priority == ALTA:
            clientesPrio.put(Client(cliente.priority,cliente.id, cliente.clientData))
        else:
             clientesNPrio.put(Client(cliente.priority,cliente.id, cliente.clientData))

def interrupt(cliente):
    if depuracao:
        printCliente(cliente, "interrompeu")
        printCliente(servidor, "foi interrompido")
    eventos.removeIfExistExitEvent()
    if isFilaUnica:
        clientesFilaUnica.put(servidor)
    elif servidor.priority == ALTA:
        clientesPrio.put(servidor)
    else:
        clientesNPrio.put(servidor)
    serverClient(cliente)
    
def serverClient(nextClient):
    global actualTime, servidor
    
    tempoExecucao = nextClient.clientData.getTimeRemaining()
    if tempoExecucao < 0:
        if nextClient.priority == ALTA:
            tempoExecucao = nextService(mi1)
        else:
            tempoExecucao = nextService(mi2)
    nextClient.clientData.service = tempoExecucao
    servidor = nextClient
    updateNextExit(tempoExecucao, nextClient)
    
    if depuracao:
        printCliente(nextClient, "executou")

def getExecutedTime():
    return actualTime - previousTime

def getRo():
    ro = [0,0]
    ro[ALTA] = tempoOcupado[ALTA]/actualTime
    ro[BAIXA] = tempoOcupado[BAIXA]/actualTime
    return ro

def updateServerExecutedTime():
    if servidor != None and previousTime != -1:
        servidor.clientData.executed += getExecutedTime()
        
def updateTimeVariables():
    updateServerExecutedTime()
    if not isFilaUnica:
        calculosMedia.updateTempoExecutando(clientesPrio.queue, getExecutedTime())
        calculosMedia.updateTempoEspera(clientesPrio.queue, getExecutedTime())
    calculosMedia.updateTempoExecutando(clientesNPrio.queue, getExecutedTime())
    calculosMedia.updateTempoEspera(clientesNPrio.queue, getExecutedTime())
    

def loopPrincipal(tamanho):
    global actualTime, previousTime, preemptive, isFilaUnica
    global n_amostras, tempoOcupado
    if(random.random() <= la1/(la1+la2)):
        updateNextArrival(ALTA, la1)
    else:
        updateNextArrival(BAIXA, la2)
    while not eventos.empty():
        eventoAtual = eventos.pop_front()
        previousTime = actualTime
        actualTime = eventoAtual.time
        if servidor != None:
            tempoOcupado[servidor.priority] += getExecutedTime()
        if depuracao:
            print("---------------------Instante: ", actualTime, "----------------------------\n")
        updateTimeVariables()
        if (eventoAtual.event == "chegada"):
            chegada(eventoAtual)
        else:            
            saida(eventoAtual, mi1)
        if depuracao :
            printDadosSistema()
        if isFilaUnica:
            plot.updateGrafosFilaUnica(clientesFilaUnica.queue, servidor, actualTime)
        else:
            plot.updateGrafos(clientesNPrio.queue, clientesPrio.queue, servidor, actualTime)
    

def imprimeTabela():
    print("\n Tabela para os valores de lamda1, lamda2, mi1, mi2 = ", la1, la2, mi1, mi2)
    calculosMedia.printTabelaFilaClasse(actualTime, totalClientes, la1, la2, mi1,mi2, preemptive, isFilaUnica)

def filaUnica():
    global actualTime, previousTime, preemptive, isFilaUnica
    global n_amostras, la2, mi2
    isFilaUnica = True
    preemptive = False
    loopPrincipal(tamanho)
    return actualTime

def filaDuplaComPreempcao():
    global actualTime, previousTime, preemptive, isFilaUnica
    global n_amostras
    isFilaUnica = False
    preemptive = True
    loopPrincipal(tamanho)

def filaDuplaSemPreempcao():
    global actualTime, previousTime, preemptive, isFilaUnica
    global n_amostras
    isFilaUnica = False
    preemptive = False
    loopPrincipal(tamanho)
    

def inicializaGlobalVariables(lambda1, lambda2, mii1, mii2, depuracaot, tamanho_t):
    global actualTime, la1, la2, mi1, mi2, eventos, clientesPrio, clientesNPrio
    global n_amostras, depuracao, todosClientes, tempoOcupado, servidor, totalClientes
    global tamanho, clientesFilaUnica, globalId
    depuracao = depuracaot
    actualTime = 0
    globalId = 0
    la1 = lambda1
    mi1 = mii1
    la2 = lambda2
    mi2 = mii2
    n_amostras = 0
    
    tamanho = tamanho_t
    todosClientes = []
    tempoOcupado = [0, 0]
    totalClientes = [0, 0]

    eventos = SLinkedList()
    servidor = None
    clientesPrio = queue.Queue()
    clientesNPrio = queue.Queue()
    clientesFilaUnica = queue.Queue()
    plot.clean()

def printCliente(cliente, evento):
    print("o cara de id: ",  cliente.id, evento)
    cliente.clientData.console()
    print("\n")
def printDadosSistema():
    if isFilaUnica:
        print("Fila: ", end = '')
        printDadosClientFila(clientesFilaUnica)
    else:
        print('Fila Alta Prioridade: ', end = '')
        printDadosClientFila(clientesPrio)
        print('Fila Baixa Prioridade: ', end = '')
        printDadosClientFila(clientesNPrio)
    if servidor != None:
        print('Servidor: {C:', servidor.clientData.arrivalTime, ", Xr:", servidor.clientData.getTimeRemaining(), "}\n")
    else: 
        print("Servidor ocioso\n")
    
def printDadosClientFila(queue):
    print("[ ", end = '')
    for client in queue.queue:
        print("{C:", client.clientData.arrivalTime, ", Xr:", client.clientData.getTimeRemaining() ,"} ", end = '')
    print("]")
        