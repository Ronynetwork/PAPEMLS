def main():
    x = 10
    soma = 0
    lista = []  # Variável não utilizada

    for x in range(x):  # Shadowing da variável 'x'
        soma =+ x  # Operador incorreto, deveria ser '+=', causando comportamento inesperado

    if soma > 50:
        return "Alto"
    elif soma < 50:
        return "Baixo"
    else:
        return soma  # Possível problema: soma pode nunca ser exatamente 50 devido ao erro acima

if __name__ == "__main__":
    resultado = main()
    print(resultado)