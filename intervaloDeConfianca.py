import math

def mediaAmostral(distribuicao):
    n = len(distribuicao)
    media = 0
    for elemento in distribuicao:
        media = media + elemento
    return media / n

def calculaIntervaloDeConfianca(distribuicao):
    # Variáveis:
    variancia = 0
    desvio = 0
    IC = 0
    n = len(distribuicao)

    tc = 1.9799 #95% de confiança e 120 graus de liberdade
    #tc = 2.6174 #99% de confiança e 120 graus de liberdade
    
    #tc = 2.0003 #95% de confiança e 60 graus de liberdade
    #tc = 2.6603 #99% de confiança e 60 graus de liberdade

    # Média Amostral
    media = mediaAmostral(distribuicao)
    # Variancia Amostral:
    for elemento in distribuicao:
        variancia = variancia + pow((elemento-media), 2)
    variancia = variancia / (n-1)

    # Desvio Padrão
    desvio = math.sqrt(variancia)
    
    # Intervalo de Confiança
    IC = tc * (desvio / math.sqrt(n))

    return IC

#calculaIntervaloDeConfianca([1,2,5,6,7,8,5,3,2,4,5,7,8])
