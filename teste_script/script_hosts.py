# Declaração da variável soma sem a palavra reservada
soma = 0

# Função que calcula a soma de números inteiros na faixa de -10 a 10
def calcular_soma():
    global soma
    
    for i in range(-10, 11):
        if i <= 0:
            soma += i
        else:
            soma -= i

# Chamada da função e imprima o resultado
calcular_soma()
print(soma)

