import requests, json

url = 'http://localhost:10012/api/generate'

erro_sq = 'Specify an exception class to catch or reraise the exception'

data = {
    "model": "llama3.2:1b", 
    "prompt": '''
Erro: {}
Codigo : except:   

NÃO USE ASTERISCOS NO CODIGO
Explique brevemente o Motivo do erro e forneça um único exemplo, siga essa ordem, sempre começando com 'Exemplo:' e apenas UM exemplo, depois o motivo do erro empre começando com 'Motivo do erro:'. 

Motivo do erro: 
Explique a causa do erro de forma objetiva AQUI. Se for necessário citar o erro exato mostrado no terminal, use aspas duplas para destacá-lo. Evite informações imprecisas ou palavras inventadas.

Exemplo:

```python
[código de exemplo ilustrando o erro]
```
    '''.format(erro_sq),
    "stream": False # Retorna toda resposta em um token
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

# def retornar_linhas(line_start, lines):
#     text = ''
#     for line in range(line_start,len(lines)):
#         text += lines[line]
#     print(text)

# print("Conteúdo da resposta:", response.text)
data = response.json()['response'] # Retorna os dados em string

# Agora, 'lines' é uma lista com cada linha do texto como um item. sem espaços vazios
lines = data.splitlines()

# Usando list compreenshion para retornar os valores necessários
lines_filtered = [line.replace('**','') for line in lines if line]

lines_filte_len = len(lines_filtered)

# Dando join pra cada dado que vinher a partir de cada linha especificada
exemplo = data.split('```')

# Divide o conteúdo nos delimitadores ``` e pega apenas o código dentro
print(data)

line_mot = [line for line in range(lines_filte_len) if lines_filtered[line] == 'Motivo de erro:']
print(line_mot)