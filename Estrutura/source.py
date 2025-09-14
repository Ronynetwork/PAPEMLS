import requests, os, base64

# Configurações do SonarQube
SONARQUBE_URL = os.getenv('SONAR_URL')
TOKEN = os.getenv('SONAR_AUTH_TOKEN')
PROJECT_KEY = os.getenv('SONAR_PROJECT_KEY')
FILE_PATH = 'teste_script/script_hosts.java'

auth_header = base64.b64encode(f"{TOKEN}:".encode()).decode()
params = {
    "project": PROJECT_KEY,
    "sort": "date",  # Ordena pela data da análise mais recente
    "statuses": "OPEN",
    "resolved": 'false'
}

def code_source(line):    
    # Requisição para pegar o código do arquivo
    response = requests.get(
        f'{SONARQUBE_URL}/api/sources/raw',  # Endpoint correto
        params={
            'key': f'{PROJECT_KEY}:{FILE_PATH}'  # Aqui é necessário usar o 'key' com o formato correto
        },
        headers = {'Authorization': f'Basic {auth_header}'}
    )

    code = response.text

    code_lines = code.splitlines()
    if line:
        line_with_error = code_lines[line-1]
    else:
        line_with_error = None
    if response.status_code == 200:
        # Se a resposta for bem-sucedida, imprime o conteúdo do arquivo
        print("Acesso ao código-fonte bem-sucedido.")
        return line_with_error# Exibe o conteúdo do arquivo
    else:
        return f"Erro {response.status_code}: {response.text}"

def code_request():
    # Função para fazer uma requisição à API do SonarQube e processar os problemas encontrados
    try:
        response = requests.get(f"{SONARQUBE_URL}/api/issues/search", 
                                params=params, 
                                headers={
                                     'Authorization': f'Basic {auth_header}'
                                })
        
        print('Requisição da análise realizada com sucesso! ', response)
    except Exception as e:
        print('Erro na requisição:', e)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Processa a resposta da API como um JSON
        arq = response.json()
        # Filtra as issues para garantir que apenas as do projeto atual sejam processadas
        try:
            filtred_issues = [issue for issue in arq.get('issues', []) if issue['project'] == PROJECT_KEY]
            print("Filtred_issues: ", filtred_issues)
        except Exception as e:
            print("Erro no filtro de issues", e)
        dict_error = {}

        if filtred_issues:
            # Itera sobre as issues filtradas
            for issue in filtred_issues:
                # print(issue)
                message = issue['message']  # Mensagem de erro do SonarQube
                line = issue.get('line') # Linha onde o problema foi identificado
                component = issue['component']  # Componente (arquivo) onde o problema está localizado
                print('Linha a ser buscada', line)
                linha_com_erro = code_source(line)
                print("Retorno do codesource: ", linha_com_erro)
                if component not in dict_error:
                    dict_error[component] = []
                else:
                    dict_error[component].append((line, message, linha_com_erro))
        print('Filtro de problemas realizado com sucesso!')

        print('A seguir, enviando dados do dicionário de issues')
        if list(dict_error.keys())[0] == f'{PROJECT_KEY}:{FILE_PATH}': # Executando e enviando todo o dicionário de dados
            msg = dict_error
        else:
            msg = f'O projeto <{PROJECT_KEY}> não possui issues abertas!'
        return msg
    else:
        # Caso a requisição não seja bem-sucedida, exibe uma mensagem de erro
        return f"Erro ao acessar o código-fonte: {response.status_code} - {response.text}"



# Chama a função para iniciar o processo de requisição e resolução de erros
try:
    print("Iniciando a requisição ao SonarQube...")
    erros = code_request()
    print("Erros sendo enviados ao flask:", erros)
    print("Requisição concluída.")
except Exception as e:
    print("Erro ao buscar informações da análise:", e)