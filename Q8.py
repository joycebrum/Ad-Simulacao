from simulador import filaDuplaComPreempcao
from simulador import filaDuplaSemPreempcao
from simulador import filaUnica
from simulador import inicializaGlobalVariables
from simulador import imprimeTabela
from variables import cenarios2


tamanho = 100

def executaCenario2FilaUnica():
    cenarios = cenarios2()
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho)
        filaUnica()

def executaCenario2FilaPreempcao():
    cenarios = cenarios2()
    #cenarios = [[0.55, 0.2, 1, 0.5]]
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho)
        filaDuplaComPreempcao()
        imprimeTabela()

def executaCenario2FilaSemPreempcao():
    cenarios = cenarios2()
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho)
        filaDuplaSemPreempcao()
        imprimeTabela()
        


def main():
    executaCenario2FilaPreempcao()
    #filaDuplaComPreempcao(la1, la2, mi1, mi2)
    #filaDuplaSemPreempcao(la1, la2, mi1, mi2)

        

main()
