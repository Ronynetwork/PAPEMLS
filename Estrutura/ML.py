import requests, json, os, html

url = 'http://localhost:10012/api/generate'
erro_sq = os.getenv('ERROR_POINT')

data = {
    "model": "llama3.2:1b", 
    "prompt": '''
Codigo com erro: except   
Erro: {}
"Explique brevemente o Motivo do erro e forneça um único exemplo, siga essa ordem, sempre começando com 'Exemplo:' e apenas UM exemplo.

Exemplo:

```python
[código de exemplo resolvendo de forma simples o erro]
```

ao fim do arquivo, dê uma breve explicação do porque o erro "{}" acontece na linha de código informada forma didática e simples. Sem adicionar erros desnecessários e que não são referentes a esse erro.

    '''.format(erro_sq, erro_sq),
    "stream": False  # Retorna toda resposta em um token
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

# print("Conteúdo da resposta:", response.text)
data = response.json()['response'] # Retorna os dados em string

# Agora, 'lines' é uma lista com cada linha do texto como um item. sem espaços vazios
lines = data.splitlines()

# Usando list compreenshion para retornar os valores necessários
lines_filtered = [line for line in lines if line]
lines_filte_len = len(lines_filtered)

# Divide o conteúdo nos delimitadores ``` e pega apenas o código dentro
exemplo_parts = data.split("```")[1]

motivo_html = [lines_filtered[line] for line in range(lines_filte_len-1,lines_filte_len)][0].replace('`', '')

print(exemplo_parts)

head = '''<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="
        default-src 'none';
        script-src 'self' 'unsafe-inline' 'unsafe-eval';
        style-src 'self' 'unsafe-inline';
        img-src 'self';
        font-src 'self';
        connect-src 'self';
        object-src 'none';
        frame-src 'self';">
    <title>Página de Erros e Soluções</title>
    <style>
        <link rel="stylesheet" href="styles.css">
    </style>
</head>
<body>
    <div class="container">
        <h2>Selecione um erro para ver a solução</h2>
        <select id="errorSelect">
            <option value="">-- Escolha um erro --</option>
'''

body = '''
</body>
</html>
    '''



option = '''

            <option value="{}">Erro: {} </option>
        </select>
        <button onclick="showSolution()">Mostrar Solução</button>

        <div id="solution" style="margin-top: 20px;"></div>
    </div>
    <script src="script.js"></script>'''.format(erro_sq, erro_sq)
    

script ='''
        function showSolution() {
            const errorType = document.getElementById("errorSelect").value;
            const solutionDiv = document.getElementById("solution");

            let solutionText = "";'''
    
            
type_erro = '''
            if (errorType === "{}") {{
                solutionText = `
                    <h3> {} </h3>
                    <p>Exemplo de Correção: </p>
                    <pre>
{}
                    </pre>
                `;
'''.format(erro_sq, motivo_html, exemplo_parts)

end_script = '''
            } else {
                solutionText = "<p>Selecione um erro para ver a solução.</p>";
            }

            solutionDiv.innerHTML = solutionText;
        }
'''

css_text = '''        
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            text-align: center;
            padding: 20px;
        }
        .container {
            background: white;
            max-width: 600px;
            margin: auto;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        select, button {
            margin-top: 10px;
            padding: 10px;
            font-size: 16px;
        }
        pre {
            background: #eee;
            padding: 10px;
            text-align: left;
            border-radius: 5px;
        }'''



html_complete = head + option + body
script_complete = script + type_erro + end_script 

# Cria o diretório se ele não existir
os.makedirs("./Estrutura/notification", exist_ok=True)

with open('./Estrutura/notification/style.css', 'w') as css:
    css.write(css_text)

with open('./Estrutura/notification/script.js', 'w') as java:
    java.write(script_complete)

with open('./Estrutura/notification/erro.html', 'w') as arquivo:
    arquivo.write(html_complete)