# Importando Bibliotecas
import os

# Receber os dados do Jenkins com os erros e arquivos a serem corrigidos
pathList = os.getenv("ERROS")
atualPath = os.path.abspath(os.getcwd()) # Pega o caminho atual
print("Caminho Atual: ", atualPath)
print("Caminho do arquivo: ")
print("Path list: ", pathList)

try:
    for obj in pathList:
        path = obj['paht']
        print("Path atual: ", path)

        for erro in obj['erros']:
            print("Erro: ", erro)
            message = erro['message']
            line = erro['line']
            corrections = erro['correction']
            print(f"Mensagem: {message}, Linha: {line}, Correções: {corrections}")
except Exception as e:
    print("Erro ao processar a lista de erros: ", e)
# Alteração de arquivos