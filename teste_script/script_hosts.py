def calcular_soma():
    total = 0
    num = int(input("Digite um número: "))
    while True:
        opcao = input("Deseja continuar? (s/n): ")
        if opcao.lower() == 's':
            total += num
            num = int(input("Digite outro número: "))
        elif opcao.lower() == 'n':
            break
        else:
            print("Opção inválida. Tente novamente.")
    print(f"O somatório dos números é: {total}")


calcular_soma()

