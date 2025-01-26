def calcular_media(valores):
    if len(valores) == 0:
        return 0  # Tratamento simples para evitar divisão por zero
    soma = 0
    for v in valores:
        soma =+ v
        print(soma)
    media = soma / len(valores)
    return media

def saudacao(nome):
    if nome == None:
        print("Olá, estranho")
    else:
        print("Olá, " + nome)

numeros = [10, 20, 30, 40, 50]
media = calcular_media(numeros)
print("A média é:", media)