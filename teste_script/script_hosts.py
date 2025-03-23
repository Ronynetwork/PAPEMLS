# Desafio: Escreva um programa que solicite a idade de 5 pessoas e mostre a soma da idades, exibindo se é maior ou menor que 60 anos.
idade_soma = 0

for _ in range(5):
    idade = int(input("Informe a idade dessa pessoa: "))
    idade_soma += idade

idade_maior_60 = False
if idade_soma > 60:
    idade_maior_60 = True

print(f"A soma das idades é {idade_soma} anos")
print(f"É maior que 60 anos? {(idade_maior_60)}")

