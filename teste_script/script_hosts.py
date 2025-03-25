# Declaração do resultado da soma com 0
resultado_soma = 0

# Funcão para calcular a soma dos números
def soma_numeros():
    # Declaração de parâmetros para calcular a soma
    num1, num2 = 5, 10
    
    global resultado_soma  # Usando a variável global para manter o valor atualizado
    
    # Cálculo da soma
    resultado_soma += (num1 + num2)
    
# Chamada da função para calcular a soma
soma_numeros()

print("O resultado final é:", resultado_soma)

