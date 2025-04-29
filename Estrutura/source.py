import requests, os, base64

# Configurações do SonarQube
SONARQUBE_URL = os.getenv('SONAR_URL')
TOKEN = os.getenv('SONAR_AUTH_TOKEN')
PROJECT_KEY = os.getenv('SONAR_PROJECT_KEY')
FILE_PATH = 'teste_script/script_hosts.java'

auth_header = base64.b64encode(f"{TOKEN}:".encode()).decode()
params = params = {
    "project": PROJECT_KEY,
    "sort": "date",  # Ordena pela data da análise mais recente
    "statuses": "OPEN",
    "resolved": 'false'
}

def resolve_error(dict_error, acao):
    # Função para resolver um erro específico no código baseado na análise do SonarQube

    # Abrir o arquivo de código e ler todas as linhas
    component_path = list(dict_error.keys())[0].replace("PAPEMLS:", "./")
    with open(component_path, 'r') as file:
        lines = file.readlines()
    messages = []
    for erros in dict_error.values():
        for line, message in erros:
            try:
                # Seleciona a linha específica onde o erro foi identificado e a divide em palavras
                if acao == "corrigir":
                    code = code_source()
                    msg = {message: code}
                    messages.append(msg)
                elif line == None:
                    messages.append({message:''})            
                else:
                    error_line = lines[line-1].strip()  # Use strip() sem argumentos
                    messages.append({message: error_line})
            except Exception as e:
                print(f"Linha {line} não encontrada no arquivo.")
    print(messages)


def code_source():    
    # Requisição para pegar o código do arquivo
    response = requests.get(
        f'{SONARQUBE_URL}/api/sources/raw',  # Endpoint correto
        params={
            'key': f'{PROJECT_KEY}:{FILE_PATH}'  # Aqui é necessário usar o 'key' com o formato correto
        },
        headers = {'Authorization': f'Basic {auth_header}'}
    )

    code = response.text

    if response.status_code == 200:
        # Se a resposta for bem-sucedida, imprime o conteúdo do arquivo
        return code# Exibe o conteúdo do arquivo
    else:
        print(f"Erro {response.status_code}: {response.text}")

def code_request(acao):
    # Função para fazer uma requisição à API do SonarQube e processar os problemas encontrados
    try:
        response = requests.get(f"{SONARQUBE_URL}/api/issues/search", 
                                params=params, 
                                headers={
                                     'Authorization': f'Basic {auth_header}'
                                })
    except Exception as e:
        print('Erro na requisição:', e)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Processa a resposta da API como um JSON
        arq = response.json()
        # Filtra as issues para garantir que apenas as do projeto atual sejam processadas
        filtred_issues = [issue for issue in arq.get('issues', []) if issue['project'] == PROJECT_KEY] 
        
        if filtred_issues:
            dict_error = {}
            # Itera sobre as issues filtradas
            for issue in filtred_issues:
                print(issue["message"])
                message = issue['message']  # Mensagem de erro do SonarQube
                line = issue.get('line')  # Linha onde o problema foi identificado
                component = issue['component']  # Componente (arquivo) onde o problema está localizado
                if component not in dict_error:
                    dict_error[component] = []
                dict_error[component].append((line, message))

        if list(dict_error.keys())[0] == f'{PROJECT_KEY}:{FILE_PATH}': # Executando e enviando todo o dicionário de dados
            resolve_error(dict_error, acao)
        else:
            print(f'O projeto <{PROJECT_KEY}> não possui issues abertas!')
    else:
        # Caso a requisição não seja bem-sucedida, exibe uma mensagem de erro
        print(f"Erro ao acessar o código-fonte: {response.status_code} - {response.text}")



# Chama a função para iniciar o processo de requisição e resolução de erros
try:
    acao = os.getenv('ACTION')
except:
    acao = ''

if __name__ == "__main__":
    code_request(acao)