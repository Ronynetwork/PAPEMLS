import requests, os, ast

url = 'http://localhost:10012/api/generate'

def type_erro(erro, motivo_html, exemplo_parts, cont):
    if cont == 0:
        type_erro = '''
            if (errorType === "{}") {{
                solutionText = `
                    <h3> {} </h3>
                    <p>Exemplo de Correção: </p>
                    <pre>
        {}
                    </pre>
                `
            }}
        '''.format(erro, motivo_html, exemplo_parts)
    else:
        type_erro = '''
            else if (errorType === "{}") {{
                solutionText = `
                    <h3> {} </h3>
                    <p>Exemplo de Correção: </p>
                    <pre>
        {}
                    </pre>
                `
            }}
        '''.format(erro, motivo_html, exemplo_parts)
    return type_erro

def option(erro) :
    option = '''
                <option value="{}">Erro: {} </option>
            '''.format(erro, erro)
    return option

try:        
    html = os.getenv("ERROR_POINT")
    erro_dict = ast.literal_eval(html)
    print('Erro dict: ', erro_dict)
    options = ''
    types = ''
    cont = 0
    for dic in erro_dict:
        for erro, code in dic.items():
            print(f"Erro: {erro}, Código: {code}")
            erro = erro.replace('"', '')
            code = code
            data = {
                "model": "llama3.2:1b", 
                "prompt": '''
                Codigo com erro: {}\nErro: {}\nExplique o motivo do erro e dê UM exemplo corrigido. Comece com 'Exemplo:' e finalize explicando por que o erro '{}' ocorre.
                '''.format(code, erro, erro),
                "temperature": 0.2,
                "num_predict": 200,
                "stream": False
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=data, headers=headers)
            print(response)

            # print("Conteúdo da resposta:", response.text)
            if response: 
                data = response.json()['response'] # Retorna os dados em string
            else:
                print("reponse inexistente")
            # Agora, 'lines' é uma lista com cada linha do texto como um item. sem espaços vazios
            print(data)
            lines = data.splitlines()

            # Usando list compreenshion para retornar os valores necessários
            lines_filtered = [line for line in lines if line]
            lines_filte_len = len(lines_filtered)

            # Divide o conteúdo nos delimitadores ``` e pega apenas o código dentro
            exemplo_parts = data.split("```")[1]
            motivo_html = [lines_filtered[line] for line in range(lines_filte_len-1,lines_filte_len)][0].replace('`', '')
            print(exemplo_parts)
            options += option(erro)
            types += type_erro(erro, motivo_html, exemplo_parts, cont)
            cont += 1
    else:   
        print("Variável ERROR_POINT não encontrada ou vazia")
except Exception as e:
    print("Projeto nao possue issues abertas!")


head = '''<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Página de Erros e Soluções</title>
</head>
<body>
    <div class="container">
        <h2>Selecione um erro para ver a solução</h2>
        <select id="errorSelect">
            <option value="">-- Escolha um erro --</option>
'''

body = '''
            </select> 
            <button onclick="showSolution()">Mostrar Solução</button>
            <div id="solution" style="margin-top: 20px;"></div>
    </div>
    <script src="{{url_for('static', filename='script.js')}}"></script>
</body>
</html>
    '''

    
script ='''
let errors = []
function showSolution() {
    const errorType = document.getElementById("errorSelect").value;
    const solutionDiv = document.getElementById("solution");

    let solutionText = "";'''
    

end_script = '''
    else {
        solutionText = "<p>Selecione um erro para ver a solução.</p>";
    }
    h2 = `
        <h2>Escolha uma ação:</h2>
        <button onclick="enviarAcao('corrigir')">Corrigir</button>
        <button onclick="enviarAcao('ignorar')">Ignorar</button>`
    
    solutionDiv.innerHTML = solutionText + h2;
    errors.push(errorType);
}

function enviarAcao(acao) {
    fetch("/receber_escolha", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "resposta": acao, "erros": errors })
    })
    .then(response => response.json())
    .then(data => alert("Escolha enviada: " + acao))
    .catch(error => console.error("Erro:", error));
}
'''


html_complete = head + options + body
script  = script + types + end_script

# Cria o diretório se ele não existir
try:
    os.makedirs('./Estrutura/notification/templates', exist_ok=True)
    os.makedirs('./Estrutura/notification/static', exist_ok=True)

    with open(os.path.join('./Estrutura/notification/static', "script.js"), 'w') as static:
        static.write(script)

    with open(os.path.join('./Estrutura/notification/templates', "erro.html"), 'w') as arquivo:
        arquivo.write(html_complete)

except Exception as e:
    print('Erro ao criar arquivos ', e)