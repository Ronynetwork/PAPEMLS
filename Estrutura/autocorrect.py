# Importando Bibliotecas
import os

# Receber os dados do Jenkins com os erros e arquivos a serem corrigidos
errosDict = os.getenv("ERROS")
atualPath = os.path.abspath(os.getcwd()) # Pega o caminho atual


# Alteração de arquivos

