import requests, os
SONARQUBE_URL = os.getenv('SONAR_URL')
TOKEN = os.getenv('sonar_token')
PROJECT_KEY = os.getenv('SONAR_PROJECT_KEY')

components_msg = {}
components = []

try:
    # Requisição para obter os problemas do projeto
    response = requests.get(f'{SONARQUBE_URL}/api/issues/search',auth=(TOKEN, ''),
                                params={
                                    'projectKeys': PROJECT_KEY,
                                    'statuses': 'OPEN',  # Para issues abertas
                                    })
    arq = response.json()
    filtred_issues = [issue for issue in arq.get('issues', []) if issue['project'] == PROJECT_KEY] # Filtrando erros e adicionando como lista para remover conflitos entre projetos
    # Separando o retorno da requisição
    for issue in filtred_issues:
        message = issue['message'] # Atribuindo mensagem de erro
        severity = issue['severity'] # Atribuindo severidade
        line = int(issue['textRange']['startLine']) # Atribuindo linha
        component = issue['component'] # Atribuindo Path
        if component not in components_msg: # Fazendo verificação se o componente ja existe no dicionario, se nao adiciona como novo dicionario na lista
            components_msg[component] = [{
            "messages": message,
            "severity": severity,
            "line": line,
            }]
        else: # se sim, adiciona a mensagem com um append
            components_msg[component].append({
                "messages": message,
                "severity": severity,
                "line": int(line), 
            })

except Exception as e:
    print(f"Erro ao obter problemas do projeto: {e}")

# definindo lista com erros
errors = []
for path in components_msg.keys(): # Fazendo for a cada chave do dicionario
    try:
        response_code = requests.get(
            f"{SONARQUBE_URL}/api/sources/raw?key={path}", # Fazendo get no codigo que foi submetido a análise
            auth=(TOKEN, '')
        )
        code = response_code.text.splitlines() # Retornando a resposta em uma lista de linhas do arquivo
        path_split = path.replace(f'{PROJECT_KEY}:', '') # Alterando o path do arquivo para remover o prefixo do projeto no sonar, deixando apenas o path limpo
        
        # Adicionando os erros à lista
        details = components_msg[path] # Definindo details como o conteudo daquele path do dicionario, ou seja, as mensagens
        for det in details: # para cada detalhe nos details eu crio um dicionario com as diretivas semelhantes ao do for anterior, porem com o path atualizado e com a linha de codigo
            error_entry = {
                "file": path_split,
                "message": det['messages'],
                "severity": det['severity'],
                "line": det['line'],
                "code": code[det['line'] - 1] if det['line'] - 1 < len(code) else "" # fazendo um tratamento lambda para buscar no codigo a linha de erro -1 o que retorna a linha exata do erro
            }
            errors.append(error_entry)
    except Exception as e:
        print(f"Erro ao obter código-fonte do componente {path}: {e}")

# Criação do conteúdo HTML
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SonarQube Notification</title>
    <link rel="stylesheet" href="style.css"> <!-- Referência ao arquivo CSS externo -->
</head>
<body>
    <div class="notification">
        <p><strong>SonarQube Issues:</strong></p>
        <button id="toggleAll" class="toggle-all">Show All</button>
'''

# Itera sobre a lista de erros para adicionar ao HTML
for index, error in enumerate(errors): # Faço um for de chave,valor e enumero a quantidade de casos do dicionario para ocorrer de forma certa, depois dou apprend nos pontos especificos
    html_content += f''' 
        <div class="error" id="error{index + 1}">
            <h3 class="error-title">{error["file"]} <span class="toggle-icon"></span></h3>
            <div class="error-details">
                <p>Message: {error["message"]} at line {error["line"]}</p>
                <p>Severity: {error["severity"]}</p>
                <p>Line in Code: {error["code"]}</p>
            </div>
        </div>
    '''

# Fechando as tags HTML e indicando arquivo js
html_content += '''
    </div>
    <script src="script_java.js"></script>
</body>
</html>
'''

# Salvando o HTML em um arquivo
path_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(path_dir, 'sonarqube-notification.html')

with open(file_path, 'w') as file:
    file.write(html_content)

print("HTML gerado com sucesso!")
