import requests, os, ast

url = 'http://localhost:10012/api/generate'
erro_sq = os.getenv('ERROR_POINT')
erro_dict = ast.literal_eval(erro_sq)
if erro_dict:
    for erro, code in erro_dict.items():
        erro = erro.replace('"', '')
        code = code
        print(f"Erro: {erro}, Código: {code}")
else:   
    print("Variável ERROR_POINT não encontrada ou vazia")

data = {
    "model": "llama3.2:1b", 
    "prompt": '''
Codigo com erro: {}   
Erro: {}
"Explique brevemente o Motivo do erro e forneça um único exemplo, siga essa ordem, sempre começando com 'Exemplo:' e apenas UM exemplo.

Exemplo:

```
[código de exemplo resolvendo de forma simples o erro]
```

ao fim do arquivo, dê uma breve explicação do porque o erro "{}" acontece na linha de código informada forma didática e simples. Sem adicionar erros desnecessários e que não são referentes a esse erro.

    '''.format(code, erro, erro),
    "stream": False  # Retorna toda resposta em um token
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

head = '''<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="
        default-src 'self';
        script-src 'self' 'unsafe-inline' 'unsafe-eval';
        style-src 'self' 'unsafe-inline';
        img-src 'self';
        font-src 'self';
        connect-src 'self';
        object-src 'none';
        frame-src 'self';">
    <link rel="stylesheet" href="style.css">
    <title>Página de Erros e Soluções</title>
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
    <script src="script.js"></script>
    '''.format(erro,erro)
    
    
script ='''
    <script>
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
                <h2>Escolha uma ação:</h2>
                <button onclick="enviarAcao('corrigir')">Corrigir</button>
                <button onclick="enviarAcao('ignorar')">Ignorar</button>
                `
'''.format(erro, motivo_html, exemplo_parts)

end_script = '''
            } else {
                solutionText = "<p>Selecione um erro para ver a solução.</p>";
            }

            solutionDiv.innerHTML = solutionText;
        }
        function enviarAcao(acao) {
            fetch("/receber_escolha", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "resposta": acao })
            })
            .then(response => response.json())
            .then(data => alert("Escolha enviada: " + acao))
            .catch(error => console.error("Erro:", error));
        }
    </script>
'''



html_complete = head + option + body
script  = script + type_erro + end_script

# Cria o diretório se ele não existir
os.makedirs("./Estrutura/notification/templates", exist_ok=True)

#  Criando Arquivo Js com os erros como opções
with open('./Estrutura/notification/templates/script.js', 'w') as arquivo:
    arquivo.write(script)

# Criando HTML
with open('./Estrutura/notification/templates/erro.html', 'w') as arquivo:
    arquivo.write(html_complete)
