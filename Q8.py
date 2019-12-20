from numpy.random import exponential
from collections import namedtuple

from LinkedList import SLinkedList
from calculosMedia import calculaTempoMedio
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
        print("prioridade: ", self.priority, " arrivalTime: ", round(self.arrivalTime,2), " timeRemaining: ", round(self.timeRemaining,2), " lastExecutedTime: ", round(self.lastExecutedTime,2))

Client = namedtuple("Client", "priority id clientData")
actualTime = 0

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
    clientData = ClientData(arrivedEvent.priority, actualTime, -1, -1)
    cliente = Client(arrivedEvent.priority, globalId, clientData)
    printCliente(cliente, "chegou")
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
    if servidor.clientData.lastExecutedTime == -1:
        executedTime = actualTime
    else:
        executedTime = actualTime - servidor.clientData.lastExecutedTime
    if servidor.id in queueTime:
        queueTime[servidor.id] += executedTime
    else:
        queueTime[servidor.id] = executedTime
    #terminando conta do tempo medio
        
    if not clientesPrio.empty() :
        #print("pegando um cliente prioritario:")
        nextClient = clientesPrio.get()
        #print("saidaaaaaa", nextClient)
        serverClient(nextClient)
    else:
        if not clientesNPrio.empty():
            #print("pegando um cliente nao prioritario:")
            nextClient = clientesNPrio.get()
            #print("saidaaaaaa", nextClient)
            nextClient.clientData.console()
            serverClient(nextClient)
        else:
            servidor = None
            #print("else")
    
def checkServer(cliente):
    global servidor
    global clientesPrio
    global clientesNPrio
    if servidor == None:
        serverClient(cliente)
    elif preemptive and cliente.priority < servidor.priority:
        interrupt(cliente)
    else:
        #print("adicionando cliente criado: ", cliente.priority, Client(cliente.priority, cliente.id, cliente.clientData))
        if cliente.priority ==0:
            clientesPrio.put(Client(cliente.priority,cliente.id, cliente.clientData))
        else:
            clientesNPrio.put(Client(cliente.priority,cliente.id, cliente.clientData))
    
def interrupt(cliente):
    printCliente(cliente, "interrompeu")
    printCliente(servidor, "foi interrompido")
    
    if servidor.clientData.lastExecutedTime == -1:
        executedTime = actualTime
    else:
        executedTime = actualTime - servidor.clientData.lastExecutedTime
    
    #fazendo conta do tempo medio do cara que ta saindo
    if servidor.id in queueTime:
        queueTime[servidor.id] += executedTime
    else:
        queueTime[servidor.id] = executedTime
    #terminando conta do tempo medio
    
    servidor.clientData.timeRemaining = servidor.clientData.timeRemaining - executedTime
    #print("interupt", servidor)
    servidor.clientData.console()
    #print("adicionando: ", servidor)
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
    nextClient.clientData.lastExecutedTime = actualTime
    servidor = nextClient
    #servidor.timeRemaining = tempoExecucao
    updateNextExit(tempoExecucao, nextClient)
    
    printCliente(nextClient, "executou")

def filaUnica(la1, mi1):
    global actualTime
    global la
    global mi
    inicializaGlobalVariables(la1, mi1)
    
    i = 0
    updateNextArrival(0, la)
    while i < 5:
        i+=1
        if not eventos.empty():
            eventoAtual = eventos.pop_front()
            actualTime = eventoAtual.time
            print("---------------------Instante: ", actualTime, "----------------------------\n")
            if (eventoAtual.event == "chegada"):
                chegada(eventoAtual, la)
            else:            
                saida(eventoAtual, mi)
            printDadosSistema()
    tempoMedioNaFila = calculaTempoMedio(queueTime)
    print(" ---------- Medias")
    print("tempo Medio na fila: ", tempoMedioNaFila)
    

def inicializaGlobalVariables(la1, mi1):
    global actualTime, la, mi, eventos, preemptive, clientesPrio, clientesNPrio, isFilaUnica
    actualTime = 0
    la = la1
    mi = mi1
    preemptive = False
    isFilaUnica = True

    eventos = SLinkedList()
    clientesPrio = queue.Queue()
    clientesNPrio = queue.Queue()

def main():
    filaUnica(1/2,1/2)

def printCliente(cliente, evento):
    print("o cara de id: ",  cliente.id, evento)
    cliente.clientData.console()
    print("\n")
def printDadosSistema():
    if not isFilaUnica:
        print('Fila Alta Prioridade: ', end = '')
        printDadosClientFila(clientesNPrio)
    print('Fila Baixa Prioridade: ', end = '')
    printDadosClientFila(clientesPrio)
    if servidor != None:
        print('Servidor: {C:', servidor.clientData.arrivalTime, ", Xr:", servidor.clientData.timeRemaining, "}\n")
    else: 
        print("servidor ocioso\n")
    
def printDadosClientFila(queue):
    print("[ ", end = '')
    for client in queue.queue:
        print("{C:", client.clientData.arrivalTime, ", Xr:", client.clientData.timeRemaining ,"} ", end = '')
    print("]")
main()
