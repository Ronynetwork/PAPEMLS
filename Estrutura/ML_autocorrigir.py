import requests, os, ast
url = 'http://localhost:10012/api/generate'
code = os.getenv("code")
try:
    erro_dict = ast.literal_eval(code)
    if erro_dict:
        for erro, code in erro_dict.items():
            erro = erro.replace('"', '')
            code = code
            print(f"Erro para ser corrigido: {erro}, Código: {code}")
    else:   
        print("Variável ERROR_POINT não encontrada ou vazia")
except Exception as e:
    print("Projeto nao possue issues abertas!")
    exit(0)


data = {
    "model": "llama3.2:1b", 
    "prompt": '''
Codigo com erro: 

{}
           
Erro: {}

ajuste ao código para apenas uma versao corrigida e funcional, nao preciso de explicação, apenas do codigo corrigido e funcional, seja o  mais assertivo possível.

    '''.format(code, erro),
    "stream": False # Retorna toda resposta em um token
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

# Dando join pra cada dado que vinher a partir de cada linha especificada

# Divide o conteúdo nos delimitadores ``` e pega apenas o código dentro

if response: 
    data = response.json()['response'] # Retorna os dados em string
    data_split = data.split('```')[1].split("\n")
    data_join = [f'{data_split[x]}\n' for x in range(1, len(data_split))]
    file_path = os.path.abspath("teste_script/script_hosts.py")
    print("Tentando acessar:", file_path)
    with open(file_path, "w") as f:
        for x in data_join:
            f.write(x)
else:
    print("response inexistente")