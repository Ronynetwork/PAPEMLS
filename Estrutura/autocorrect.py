# Importando Bibliotecas
import os

# Receber os dados do Jenkins com os erros e arquivos a serem corrigidos
errosDict = os.getenv("ERROS")
atualPath = os.path.abspath(os.getcwd()) # Pega o caminho atual
print("Caminho Atual: ", atualPath)
print("Erros Dict: ", errosDict)


# Alteração de arquivos

