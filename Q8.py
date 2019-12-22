from simulador import filaDuplaComPreempcao
from simulador import filaDuplaSemPreempcao
from simulador import filaUnica
from simulador import inicializaGlobalVariables


tamanho = 100
def cenarios2():
    la = 0.05
    cenarios = []
    for i in range (0, 11):
       cenarios.append([round(la + la*i, 2), 0.2, 1, 0.5])
    return cenarios

def executaCenario2FilaUnica():
    cenarios = cenarios2()
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False)
        la = cenario[0] + cenario[1]
        mi = cenario[2] + cenario[3]
        filaUnica(la, mi, tamanho)

def executaCenario2FilaPreempcao():
    cenarios = cenarios2()
    for cenario in cenarios:
        inicializaGlobalVariables(cenario[0], cenario[1], 
                                  cenario[2], cenario[3], 
                                  False)
        filaDuplaComPreempcao(cenario[0], cenario[1], 
                              cenario[2], cenario[3], 
                              tamanho)


def main():
    executaCenario2FilaPreempcao()
    #filaDuplaComPreempcao(la1, la2, mi1, mi2, tamanho)
    #filaDuplaSemPreempcao(la1, la2, mi1, mi2, tamanho)

        

main()
