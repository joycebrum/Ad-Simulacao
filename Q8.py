from simulador import filaDuplaComPreempcao
from simulador import filaDuplaSemPreempcao
from simulador import filaUnica
from simulador import inicializaGlobalVariables


tamanho = 100
def cenarios2():
    la = 0.05
    cenarios = []
    for i in range (0, 12):
       cenarios.append([round(la + la*i, 2), 0.2, 1, 0.5])
    return cenarios

def executaCenario2FilaUnica():
    cenarios = cenarios2()
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho)
        la = cenario[0] + cenario[1]
        mi = cenario[2] + cenario[3]
        filaUnica(la, mi)

def executaCenario2FilaPreempcao():
    cenarios = cenarios2()
    #cenarios = [[0.55, 0.2, 1, 0.5]]
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho)
        filaDuplaComPreempcao(cenario[0], cenario[1], 
                              cenario[2], cenario[3])

def executaCenario2FilaSemPreempcao():
    cenarios = cenarios2()
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False, tamanho)
        filaDuplaSemPreempcao(cenario[0], cenario[1], 
                              cenario[2], cenario[3])


def main():
    executaCenario2FilaPreempcao()
    #filaDuplaComPreempcao(la1, la2, mi1, mi2)
    #filaDuplaSemPreempcao(la1, la2, mi1, mi2)

        

main()
