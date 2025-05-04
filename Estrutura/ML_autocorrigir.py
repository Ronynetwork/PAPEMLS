import requests, os, ast

url = 'http://localhost:10012/api/generate'

try:
    file_path = os.path.abspath("teste_script/script_hosts.java")
    with open(file_path, "r") as f:
        code = f.read()
    erro_dict = ast.literal_eval(os.getenv("ERROR_POINT"))
    erros_escolhidos = ast.literal_eval(os.getenv("ERROS"))
    for erro in erros_escolhidos:
        erro_limpo = erro.replace('"', '').strip()
        for err in erro_dict:
            for chave in err.keys():
                chave_limpa = chave.replace('"', '').strip()
                if erro_limpo == chave_limpa:
                    code_error = err[chave]
                    print(f"Erro para ser corrigido: {erro}, Código: {code}")

                    data = {
                        "model": "codellama:7b",
                        "prompt": f"""
                        Fix the following Java code with this error {erro} IN this line {code_error}. Return ONLY the fixed code. No explanations, no comments.

                        {code}
                        """,
                        "stream": False
                    }


                    headers = {
                        "Content-Type": "application/json"
                    }
                    print(f"chegou aq")
                    response = requests.post(url, json=data, headers=headers)

                    print(response.status_code, response)
                    if response: 
                        data = response.json()['response'] # Retorna os dados em string
                        data_split = data.split('```')[1].split("\n")
                        data_join = [f'{data_split[x]}\n' for x in range(1, len(data_split))]

                        print("Tentando acessar:", file_path)
                        with open(file_path, "w") as f:
                            for x in data_join:
                                f.write(x)
                    else:
                        print("response inexistente")
    else:   
        print("Variável ERROR_POINT não encontrada ou vazia")
except Exception as e:
    print("Projeto nao possue issues abertas!")
    exit(0)


# Dando join pra cada dado que vinher a partir de cada linha especificada

# Divide o conteúdo nos delimitadores ``` e pega apenas o código dentro
