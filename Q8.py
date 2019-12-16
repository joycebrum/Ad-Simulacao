from numpy.random import exponential
from collections import namedtuple

from LinkedList import SLinkedList
import queue

la = 1/2
mi = 1/2
Evento = namedtuple("Evento", "time event priority") 
class ClientData :
    def __init__(self, priority = 0, arrivalTime=-1, timeRemaining = -1, lastExecutedTime = -1):
        self.priority = priority 
        self.arrivalTime = arrivalTime
        self.timeRemaining = timeRemaining 
        self.lastExecutedTime = lastExecutedTime
    def console(self):
        print("prioridade: ", self.priority, " arrivalTime: ", self.arrivalTime, " timeRemaining: ", self.timeRemaining, " lastExecutedTime: ", self.lastExecutedTime)

Client = namedtuple("Client", "priority clientData")
actualTime = 0

isFilaUnica = True
preemptive = False

eventos = SLinkedList()
clientes = queue.PriorityQueue(7000)
servidor = None

def nextArrival(la):
    return exponential(1/la)

def nextService(mi):
    return exponential(1/mi)

def chegada(arrivedEvent, la):
    global actualTime
    updateNextArrival(arrivedEvent.priority, la)
    clientData = ClientData(arrivedEvent.priority, actualTime, -1, -1)
    checkServer(clientData)
    
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
    servidor.console()
    if not clientes.empty() :
        nextClient = clientes.get()
        print("saidaaaaaa", nextClient)
        nextClient.console()
        serverClient(nextClient)
    else:
        servidor = None
        print("else")
    
def checkServer(clientData):
    global servidor
    global clientes
    if servidor == None:
        serverClient(clientData)
    elif preemptive and clientData.priority < servidor.priority:
        interrupt(clientData)
    else:
        clientes.put(clientData.priority, Client(clientData.priority, clientData))
    
def interrupt(clientData):
    executedTime = actualTime - servidor.lastExecutedTime
    servidor.timeRemaining = servidor.timeRemaining - executedTime
    print("interupt", servidor)
    servidor.console()
    clientes.put(servidor.priority, servidor)
    serverClient(clientData)
    
def serverClient(nextClient):
    global actualTime
    global servidor
    tempoExecucao = nextClient.timeRemaining
    if tempoExecucao < 0:
        tempoExecucao = nextService(mi)
    nextClient.timeRemaining = tempoExecucao
    servidor = nextClient
    #servidor.timeRemaining = tempoExecucao
    updateNextExit(tempoExecucao, nextClient)

def main():
    global actualTime
    actualTime = 0
    global la
    global mi
    i = 0
    updateNextArrival(0, la)
    while i < 5:
        i+=1
        if not eventos.empty():
            eventoAtual = eventos.pop_front()
            actualTime = eventoAtual.time
            if (eventoAtual.event == "chegada"):
                #print(actualTime, "chegada")
                chegada(eventoAtual, la)
            else:            
                #print(actualTime, "saida")
                saida(eventoAtual, mi)
        #print('\n')
    print("fim")
    
    
main()
