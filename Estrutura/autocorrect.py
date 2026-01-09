# Importando Bibliotecas
import os, json, re, logging

#Configurações de logging
logger = logging.getLogger(__file__.split("/")[-1])
logging.basicConfig(encoding="utf-8", level=logging.INFO)

# Receber os dados do Jenkins com os erros e arquivos a serem corrigidos
pathList_raw = os.getenv("ERROS")  # isso é uma string
pathList = json.loads(pathList_raw)  # agora é uma lista de dicionários
atualPath = os.path.abspath(os.getcwd()) # Pega o caminho atual
logger.info("Caminho Atual: %s", atualPath) # Usando o %s para indicar uma concatenação com string e evitar custos de string no log
logger.info("Path list: %s", pathList)

# Exibir os dados recebidos para verificação
try:
    for obj in pathList:    
        pathBrute = obj['path']
        pathFinal = pathBrute.split(":")[1]
        logger.info("Path atual: %s", pathFinal)

        for erro in obj['errors']: # Percorre a lista de erros e define as correções
            # print("Erro: ", erro)
            message = erro['message']
            line = erro['line']
            correction = erro['correction']
            # print(f"Mensagem: {message}, Linha: {line}, Correções: {corrections}")

            with open(pathFinal, 'r+') as file: # Abre o arquivo para escrita e itera sobre as linhas para aplicar as correções
                file_lines = file.readlines()
                logger.info("Linhas do arquivo antes da correção: %s", file_lines)
                for l, content in enumerate(file_lines, start=1): # Percorre cada linha do arquivo onde L vira a linha e content o conteudo
                    if l == line:
                        # Corrigindo identação antes de alterar
                        logger.info("Aplicando correção na linha %s: %s", line, correction)

            # captura os espaços/tabs iniciais com método GROUP e utiliza -1 nas linhas do arquivo indicando a linha exata de alteração
                        indentacao = re.match(r'^\s*', file_lines[l-1]).group()
                        correction_complete = ''
                        # Verificando se a correção necessita da alteração de mais de uma linha
                        if len(correction.split("\n")) > 1:
                            correctionList =  correction.split("\n")
                            for correction in correctionList:
                                correction_complete += indentacao + correction + '\n'
                        else:
                            correction_complete = indentacao + correction + '\n'
                        file_lines[l-1] =  correction_complete # Substitui a linha com a correção e adiciona quebra de linha

                logger.info("Linhas do arquivo após a correção: %s", file_lines)
                file.seek(0) # Move o cursor para o início do arquivo
                file.writelines(file_lines) # Escreve as linhas corrigidas de volta ao arquivo
                file.truncate() # Remove qualquer conteúdo restante após a escrita
                logger.info("Arquivo %s corrigido com sucesso.", pathFinal)
except Exception as e:
    print("Erro ao processar a lista de erros   : ", e)