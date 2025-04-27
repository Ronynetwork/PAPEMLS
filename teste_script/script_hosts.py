def main():
    x = 10
    soma = 0
    
    for _ in range(x):
        # Errado: 'soma' não está dentro de uma variável global ou lambda
        soma += x  
    
    if soma > 50:
        return "Alto"
    elif soma < 50:
        return "Baixo"
    else:
        return soma  

if __name__ == "__main__":
    resultado = main()
    verifica = resultado.verifica()
    print(resultado)  

