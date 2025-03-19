import requests, os, ast
url = 'http://localhost:10012/api/generate'
code = os.getenv("code")
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
Codigo com erro: 

{}
           
Erro: {}

ajuste a parte do código que se refere ao erro.

    '''.format(code, erro),
    "stream": False # Retorna toda resposta em um token
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

print(response)
# print("Conteúdo da resposta:", response.text)
data = response.json()['response'] # Retorna os dados em string

# Dando join pra cada dado que vinher a partir de cada linha especificada
exemplo = data.split('```')[1]

# Divide o conteúdo nos delimitadores ``` e pega apenas o código dentro
if response: 
    data = response.json()['response'] # Retorna os dados em string
    exemplo = data.split('```')[1]
    with open("Estrutura/teste_script/script_hosts.py", "w") as f:
        f.write(exemplo)
else:
    print("response inexistente")