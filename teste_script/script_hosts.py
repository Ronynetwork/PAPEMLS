n = int(input("Digite um número: "))

soma = 0

while n != 0:
    soma += n
    n = int(input("Digite outro número para somar (ou 0 para parar): "))
    
if n == 0:
    print("A soma é igual a", soma)
else:
    print("Não possível calcular a soma.")

