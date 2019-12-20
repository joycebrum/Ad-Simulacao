from numpy.random import exponential
from collections import namedtuple

from LinkedList import SLinkedList
from calculosMedia import calculaTempoMedio
from calculosMedia import updateTempoEspera
from calculosMedia import updateTempoExecutando
from calculosMedia import numeroMedioPessoasNaFila
import queue
import random

BAIXA = 1
ALTA = 0

la1 = 0
mi1 = 0
la2 = 0
mi2 = 0

todosClientes = []
Evento = namedtuple("Evento", "time event priority") 
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

globalId = 0

queueTime = {}
servidor = None

def nextArrival(la):
    return exponential(1/la)

def nextService(mi):
    return exponential(1/mi)

def chegada(arrivedEvent, la):
    global actualTime
    global globalId
    updateNextArrival(arrivedEvent.priority, la)
    clientData = ClientData(arrivedEvent.priority, actualTime, -1)
    cliente = Client(arrivedEvent.priority, globalId, clientData)
    printCliente(cliente, "chegou")
    todosClientes.append(cliente)
    globalId+=1
    checkServer(cliente)
    
    
def updateNextArrival(priority, la):
    nextA = nextArrival(la)
    proximaChegada = Evento(actualTime + nextA, "chegada", priority)
    eventos.add(proximaChegada)
    
def updateNextExit(tempoExecucao, nextClient):
    interruption = eventos.getInterruption(actualTime + tempoExecucao, nextClient.priority)
    if interruption == None or not preemptive: #so adiciona evento de saida se nao for ser interrompido
        return eventos.add(Evento(actualTime + tempoExecucao, "saida", nextClient.priority))

def saida(exitEvent, mi):
    global servidor
    printCliente(servidor, "saiu")
    
    #fazendo conta do tempo medio do cara que ta saindo
    if servidor.id in queueTime:
        queueTime[servidor.id] += getExecutedTime()
    else:
        queueTime[servidor.id] = getExecutedTime()
    #terminando conta do tempo medio
        
    if not clientesPrio.empty() :
        nextClient = clientesPrio.get()
        serverClient(nextClient)
    else:
        if not clientesNPrio.empty():
            nextClient = clientesNPrio.get()
            nextClient.clientData.console()
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
        if cliente.priority == ALTA:
            clientesPrio.put(Client(cliente.priority,cliente.id, cliente.clientData))
        else:
             clientesNPrio.put(Client(cliente.priority,cliente.id, cliente.clientData))

def interrupt(cliente):
    printCliente(cliente, "interrompeu")
    printCliente(servidor, "foi interrompido")
   
    #fazendo conta do tempo medio do cara que ta saindo
    if servidor.id in queueTime:
        queueTime[servidor.id] += getExecutedTime()
    else:
        queueTime[servidor.id] = getExecutedTime()
    #terminando conta do tempo medio
    
    if servidor.priority == ALTA:
        clientesPrio.put(servidor)
    else:
        clientesNPrio.put(servidor)
    serverClient(cliente)
    
def serverClient(nextClient):
    global actualTime
    global servidor
    
    tempoExecucao = nextClient.clientData.getTimeRemaining()
    if tempoExecucao < 0:
        tempoExecucao = nextService(mi1)
    nextClient.clientData.service = tempoExecucao
    servidor = nextClient
    updateNextExit(tempoExecucao, nextClient)
    
    printCliente(nextClient, "executou")

def getExecutedTime():
    return actualTime - previousTime

def updateServerExecutedTime():
    if servidor != None and previousTime != -1:
        servidor.clientData.executed += getExecutedTime()
        
def updateTimeVariables():
    updateServerExecutedTime()
    if not isFilaUnica:
        updateTempoExecutando(clientesPrio.queue, getExecutedTime())
        updateTempoEspera(clientesPrio.queue, getExecutedTime())
    updateTempoExecutando(clientesNPrio.queue, getExecutedTime())
    updateTempoEspera(clientesNPrio.queue, getExecutedTime())
    
    
def filaUnica(la1, mi1, tamanho):
    global actualTime, previousTime, preempitve, isFilaUnica
    isFilaUnica = True
    preemptive = False
    i = 0
    updateNextArrival(BAIXA, la1)
    while i < tamanho:
        i+=1
        if not eventos.empty():
            eventoAtual = eventos.pop_front()
            previousTime = actualTime
            actualTime = eventoAtual.time
            print("---------------------Instante: ", actualTime, "----------------------------\n")
            updateTimeVariables()
            if (eventoAtual.event == "chegada"):
                chegada(eventoAtual, la1)
            else:            
                saida(eventoAtual, mi1)
            printDadosSistema()
    tempoMedioNaFila = calculaTempoMedio(queueTime)
    print(" ---------- Medias")
    print("E[W] = ", tempoMedioNaFila)
    print("E[T] = ", numeroMedioPessoasNaFila(todosClientes, actualTime))

def filaDuplaComPreempcao(la1, la2, mi1, mi2, tamanho):
    global actualTime, previousTime, preempitve, isFilaUnica
    isFilaUnica = False
    preemptive = True

    i=0

    if(random.random() <= la1/(la1+la2)):
        updateNextArrival(ALTA, la1)
    else:
        updateNextArrival(BAIXA, la2)
    eventos.console()
    print("INICIO")
    while i < tamanho:
        eventos.console()
        if not eventos.empty():
            eventoAtual = eventos.pop_front()
            previouseTime = actualTime
            actualTime = eventoAtual.time
            print("---------------------Instante: ", actualTime, "----------------------------\n")
            updateTimeVariables()
            if (eventoAtual.event == "chegada"):
                chegada(eventoAtual, la1)
            else:            
                saida(eventoAtual, mi1)
            printDadosSistema()
    tempoMedioNaFila = calculaTempoMedio(queueTime)
    print(" ---------- Medias")
    print("E[W] = ", tempoMedioNaFila)
    print("E[T] = ", numeroMedioPessoasNaFila(todosClientes, actualTime))
    print(1)

def inicializaGlobalVariables(lambda1, lambda2, mii1, mii2):
    global actualTime, la1, la2, mi1, mi2, eventos, clientesPrio, clientesNPrio
    actualTime = 0
    la1 = lambda1
    mi1 = mii1
    la2 = lambda2
    mi2 = mii2

    eventos = SLinkedList()
    clientesPrio = queue.Queue()
    clientesNPrio = queue.Queue()

def main():
    global la
    global mi
    la1 = 20 #0.05
    mi1 = 1 #1
    la2 = 20 #0.2
    mi2 = 1 #0.5
    
    tamanho = 100
    
    inicializaGlobalVariables(la1, la2, mi1, mi2)
    #filaUnica(la1, mi1, tamanho)
    filaDuplaComPreempcao(la1, la2, mi1, mi2, tamanho)

def printCliente(cliente, evento):
    print("o cara de id: ",  cliente.id, evento)
    cliente.clientData.console()
    print("\n")
def printDadosSistema():
    if not isFilaUnica:
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
main()
