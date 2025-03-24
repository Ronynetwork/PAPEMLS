# Início do programa
media = 0

# Calcula a soma dos valores da lista
def calcular_soma():
    global media
    if len(lista) == 0:
        print("A lista está vazia")
    else:
        media = sum(lista) / len(lista)

# Exibe a mensagem de erro
print("Erro: Remove o local variable soma.")

# Início do main
lista = []
while True:
    escolha = input("Escolha uma opção:\n1 - Adicionar valor\n2 - Calcular média\n3 - Sair\n")
    if escolha == "1":
        valor = float(input("Insira o valor: "))
        lista.append(valor)
    elif escolha == "2" and len(lista) > 0:
        calcular_soma()
        print(f"A média é: {media:.2f}")
    elif escolha == "3":
        break
    else:
        print("Opção inválida. Tente novamente.")

# Fim do main
print("Fim do programa.")

