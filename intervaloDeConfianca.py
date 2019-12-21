import math

def calculaIntervaloDeConfianca(distribuicao):
    # Variáveis:
    media = 0
    variancia = 0
    desvio = 0
    IC = 0
    n = len(distribuicao)

    tc = 1.9799 #95% de confiança e 120 graus de liberdade
    #tc = 2.6174 #99% de confiança e 120 graus de liberdade
    
    #tc = 2.0003 #95% de confiança e 60 graus de liberdade
    #tc = 2.6603 #99% de confiança e 60 graus de liberdade

    # Média Amostral
    print("fazendo a média")
    for elemento in distribuicao:
        media = media + elemento
    media = media / n

    # Variancia Amostral:
    print("fazendo a variancia")
    for elemento in distribuicao:
        variancia = variancia + pow((elemento-media), 2)
    variancia = variancia / (n-1)

    # Desvio Padrão
    print("fazendo o desvio")
    desvio = math.sqrt(variancia)
    
    # Intervalo de Confiança
    print("fazendo o intervalo")
    print("tc = ", tc, " desvio = ", desvio, "raiz(n) = ", math.sqrt(n))
    IC = tc * (desvio / math.sqrt(n))

    print("retornando IC = ", IC)
    return IC

calculaIntervaloDeConfianca([1,2,5,6,7,8,5,3,2,4,5,7,8])
