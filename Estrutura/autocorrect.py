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

        for erro in obj['errors']: # Percorre a lista de erros e define as correções
            # print("Erro: ", erro)
            message = erro['message']
            line = erro['line']
            correction = erro['correction']
            # print(f"Mensagem: {message}, Linha: {line}, Correções: {corrections}")

            with open(path, 'r+') as file: # Abre o arquivo para escrita e itera sobre as linhas para aplicar as correções
                file_lines = file.readlines()
                print("Linhas do arquivo antes da correção: ", file_lines)
                for l, content in enumerate(file_lines, start=0): # Percorre cada linha do arquivo
                    print("Linha atual do arquivo: ", l, " Linha do erro: ", line)
                    if l == line:
                        print(f"Aplicando correção na linha {line}: {correction}")
                        file_lines[l] = correction # Substitui a linha com a correção
                print("Linhas do arquivo após a correção: ", file_lines)
                file.seek(0) # Move o cursor para o início do arquivo
                file.writelines(file_lines) # Escreve as linhas corrigidas de volta ao arquivo
                file.truncate() # Remove qualquer conteúdo restante após a escrita
                print(f"Arquivo {path} corrigido com sucesso.")
except Exception as e:
    print("Erro ao processar a lista de erros   : ", e)
# Alteração de arquivos