from simulador import filaDuplaComPreempcao
from simulador import filaDuplaSemPreempcao
from simulador import filaUnica
from simulador import inicializaGlobalVariables
from simulador import imprimeTabela
from variables import cenarios2
from variables import cenarios3


tamanho = 1000

def executaCenarioFilaUnica(cenarios, tipo):
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho, tipo)
        filaUnica()
        imprimeTabela()

def executaCenarioFilaPreempcao(cenarios, tipo):
    #cenarios = [[0.55, 0.2, 1, 0.5]]
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho, tipo)
        filaDuplaComPreempcao()
        imprimeTabela()

def executaCenarioFilaSemPreempcao(cenarios, tipo):
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho, tipo)
        filaDuplaSemPreempcao()
        imprimeTabela()
        


def main():
    executaCenarioFilaSemPreempcao(cenarios3(),'d')
    #filaDuplaComPreempcao(la1, la2, mi1, mi2)
    #filaDuplaSemPreempcao(la1, la2, mi1, mi2)

        

main()
