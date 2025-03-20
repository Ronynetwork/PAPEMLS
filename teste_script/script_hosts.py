def dividir(a, b):
    return a / b  # Erro: Possível divisão por zero não tratada

def main():
    x = 10
    y = 0  # Variável com valor que causará a exceção
    print("Divisão:", dividir(x, y))

if __name__ == "__main__":
    main()
