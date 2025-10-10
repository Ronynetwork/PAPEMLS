# Importando Bibliotecas
import os, json

# Receber os dados do Jenkins com os erros e arquivos a serem corrigidos
pathList_raw = os.getenv("ERROS")  # isso é uma string
pathList = json.loads(pathList_raw)  # agora é uma lista de dicionários
atualPath = os.path.abspath(os.getcwd()) # Pega o caminho atual
print("Caminho Atual: ", atualPath)
print("Caminho do arquivo: ")
print("Path list: ", pathList)

# Exibir os dados recebidos para verificação
try:
    for obj in pathList:
        path = obj['path']
        print("Path atual: ", path)

        for erro in obj['errors']:
            print("Erro: ", erro)
            message = erro['message']
            line = erro['line']
            corrections = erro['correction']
            print(f"Mensagem: {message}, Linha: {line}, Correções: {corrections}")
except Exception as e:
    print("Erro ao processar a lista de erros: ", e)
# Alteração de arquivos