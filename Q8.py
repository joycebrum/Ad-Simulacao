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
clientesPrio = queue.Queue()
clientesNPrio = queue.Queue()
#clientes = queue.PriorityQueue(7000)
servidor = None

def nextArrival(la):
    return exponential(1/la)

def nextService(mi):
    return exponential(1/mi)

def chegada(arrivedEvent, la):
    global actualTime
    updateNextArrival(arrivedEvent.priority, la)
    clientData = ClientData(arrivedEvent.priority, actualTime, -1, -1)
    cliente = Client(arrivedEvent.priority, clientData)
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
    servidor.clientData.console()
    if not clientesPrio.empty() :
        print("pegando um cliente prioritario:")
        nextClient = clientesPrio.get()
        print("saidaaaaaa", nextClient)
        nextClient.clientData.console()
        serverClient(nextClient)
    else:
        if not clientesNPrio.empty():
            print("pegando um cliente nao prioritario:")
            nextClient = clientesNPrio.get()
            print("saidaaaaaa", nextClient)
            nextClient.clientData.console()
            serverClient(nextClient)
        else:
            servidor = None
            print("else")
    
def checkServer(cliente):
    global servidor
    global clientesPrio
    global clientesNPrio
    if servidor == None:
        serverClient(cliente)
    elif preemptive and cliente.priority < servidor.priority:
        interrupt(cliente)
    else:
        print("adicionando cliente criado: ", cliente.priority, Client(cliente.priority, cliente.clientData))
        if cliente.priority ==0:
            clientesPrio.put(Client(cliente.priority, cliente.clientData))
        else:
            clientesNPrio.put(Client(cliente.priority, cliente.clientData))
    
def interrupt(cliente):
    executedTime = actualTime - servidor.lastExecutedTime
    servidor.clientData.timeRemaining = servidor.clientData.timeRemaining - executedTime
    print("interupt", servidor)
    servidor.clientData.console()
    print("adicionando: ", servidor)
    if servidor.priority ==0:
        clientesPrio.put(servidor)
    else:
        clientesNPrio.put(servidor)
    #clientes.put(servidor.priority, servidor)
    serverClient(cliente)
    
def serverClient(nextClient):
    global actualTime
    global servidor
    tempoExecucao = nextClient.clientData.timeRemaining
    if tempoExecucao < 0:
        tempoExecucao = nextService(mi)
    nextClient.clientData.timeRemaining = tempoExecucao
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
