import requests, difflib, os

# Configurações do SonarQube
SONARQUBE_URL = os.getenv('SONAR_URL')
TOKEN = os.getenv('SONAR_AUTH_TOKEN')
PROJECT_KEY = os.getenv('SONAR_PROJECT_KEY')

# SONARQUBE_URL = 'http://localhost:9000'
# PROJECT_KEY = 'PAPEMLS'

def resolve_error(component, line, message):
    # Função para resolver um erro específico no código baseado na análise do SonarQube
    component_path =  component.replace(f'{PROJECT_KEY}:', './')
    similaridade_minima = 0.49  # Define o limite mínimo de similaridade (0 a 1) para considerar duas palavras como similares
    # Abrir o arquivo de código e ler todas as linhas
    with open(component_path, 'r') as file:
        lines = file.readlines()
    # Seleciona a linha específica onde o erro foi identificado e a divide em palavras
    error_line = lines[line-1].split()
    msg = dict()
    msg[message]=error_line[0]
    print(msg)


def code_request():
    # Função para fazer uma requisição à API do SonarQube e processar os problemas encontrados
    
    try:
        # Realiza uma requisição GET à API do SonarQube para buscar problemas no código do projeto especificado
        response = requests.get(f'{SONARQUBE_URL}/api/issues/search', auth=(TOKEN, ''),
                                params={
                                    'projectKeys': PROJECT_KEY,
                                    'statuses': 'OPEN',  # Filtra para issues abertas
                                })
    except Exception as e:
        print('Erro na requisição ')
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Processa a resposta da API como um JSON
        arq = response.json()
        # Filtra as issues para garantir que apenas as do projeto atual sejam processadas
        filtred_issues = [issue for issue in arq.get('issues', []) if issue['project'] == PROJECT_KEY] 
        
        if filtred_issues:
            # Itera sobre as issues filtradas
            for issue in filtred_issues:
                message = issue['message']  # Mensagem de erro do SonarQube
                line = issue.get('line')  # Linha onde o problema foi identificado
                component = issue['component']  # Componente (arquivo) onde o problema está localizado
                if component == f'{PROJECT_KEY}:teste_script/script_hosts.py':
                    resolve_error(component, line, message)
        else:
            print(f'O projeto <{PROJECT_KEY}> não possui issues abertas!')
    else:
        # Caso a requisição não seja bem-sucedida, exibe uma mensagem de erro
        print(f"Erro ao acessar o código-fonte: {response.status_code} - {response.text}")

# Chama a função para iniciar o processo de requisição e resolução de erros
code_request()
