from openai import OpenAI
import os, ast

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
    if html:
        # Buscando a API key do OpenRouter via Jenkins
        API_KEY = os.getenv("API_KEY")
        print('API_KEY: ', API_KEY)

        erro_dict = ast.literal_eval(html)
        print('Erro dict: ', erro_dict)
        options = ''
        types = ''
        cont = 0
        print(10*'-')
        API_KEY = os.getenv("API_KEY")
        print(API_KEY)
        for dic in erro_dict:
            for erro, code in dic.items():
                print(f"Erro: {erro}, Código: {code}")
                erro = erro.replace('"', '')
                code = code
                try:
                    client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=API_KEY,
                    )

                    completion = client.chat.completions.create(
                        #   extra_headers={
                        #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                        #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
                        #   },
                        model="meta-llama/llama-3.3-8b-instruct:free",
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
                                Você é um agente de correção de código.  
                                Corrija o trecho abaixo conforme o erro informado.

                                Erro: {erro}
                                Código: {code}

                                Responda SEMPRE usando o seguinte formato, sem textos extras:

                                Explication: (Explique brevemente a correção realizada, em uma linha)
                                Correction:
                                <coloque aqui o código corrigido>

                                Exemplo:
                                Explication: O construtor BigDecimal(double) foi substituído por BigDecimal.valueOf(double) para evitar imprecisão.
                                Correction:
                                BigDecimal bd1 = BigDecimal.valueOf(d);

                                Agora, gere sua resposta:
                                Erro: {erro}
                                Código: {code}
                                """
                                # ...existing code...
                            }
                        ]
                    )
                except Exception as e:
                    print("Erro ao chamar a API do OpenAI: ", e)
                    continue
                
                response = completion.choices[0].message.content # Retorna os dados em string
                print('Response: \n', response)
                # print("Conteúdo da resposta:", response.text)
                if response: 
                    data = response
                else:
                    print("reponse inexistente")
                # Agora, 'lines' é uma lista com cada linha do texto como um item. sem espaços vazios
                lines = data.splitlines()
                # Usando list compreenshion para retornar os valores necessários
                lines_filtered = [line for line in lines if line]
                lines_filte_len = len(lines_filtered)
                if 'Correction:' in data:
                    exemplo_parts = data.split("Correction:")[1]
                    print('Exemplo parts: ', exemplo_parts)
                else:
                    exemplo_parts = ''

                # Para a explicação final:
                if 'Explication:' in data:
                    motivo_html = data.split("Explication:")[1].strip()
                    print('Motivo html: ', motivo_html)

                options += option(erro)
                types += type_erro(erro, motivo_html, exemplo_parts, cont)
                cont += 1
        else:
            print("Nenhum erro encontrado no dicionário.")
    else:   
        print("Variável ERROR_POINT não encontrada ou vazia")
except Exception as e:
    print("Errp indicado: ", e)


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