import requests, json, os

url = 'http://localhost:10012/api/generate'
erro_sq = 'Specify an exception class to catch or reraise the exception'
data = {
    "model": "llama3.2:1b", 
    "prompt": '''Erro: {}
    codigo: except:
    me informe rapidamente qual sentido do aviso e uma sujestao de ajuste, divida em duas partes, ERRO: e EXPLICAÇÃO:
    cite apenas um exemplo na explicação. Na parte de erro, explique brevemente o erro mas nao cite exemplos.'''.format(erro_sq),
    "stream": False
}
headers = {
    "Content-Type": "application/json"
}

# Enviando conteudo para IA
response = requests.post(url, json=data, headers=headers)
text = ''

response = response.json()
text += f"{response.get('response')}"
print(text)

head = '''<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página de Erros e Soluções</title>
    <style>
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
        }
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

message = response['message']['content']
expliq_line = message.find('EXPLICAÇÃO:')
#print(message)
erro =  ''.join(message[:expliq_line-1].split('\n')).replace('*','')
print(erro)

option = '''

            <option value="{}">Erro: {} </option>
        </select>
        <button onclick="showSolution()">Mostrar Solução</button>

        <div id="solution" style="margin-top: 20px;"></div>
    </div>'''.format(erro_sq, erro_sq)

script ='''<script>
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
try:
    x = int("abc")
except ValueError:
    print("Erro: Valor inválido!")
                    </pre>
                `;

'''.format(erro_sq, erro)

end_script = '''
            } else {
                solutionText = "<p>Selecione um erro para ver a solução.</p>";
            }

            solutionDiv.innerHTML = solutionText;
        }
    </script>
'''

html_complete = head + option + script + type_erro + end_script + body


with open('notification/erro.html', 'w') as arquivo:
    arquivo.write(html_complete)
    arquivo.close()
# or access fields directly from the response object
# print(response.message.content)