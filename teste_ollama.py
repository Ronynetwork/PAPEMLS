import requests, json

url = 'http://localhost:10012/api/generate'

erro_sq = 'Specify an exception class to catch or reraise the exception'

data = {
    "model": "llama3.2:1b", 
    "prompt": '''Erro: {}
    codigo: 'except:'
    me informe rapidamente descrição breve do motivo do e um único exemplo.
    cite apenas um exemplo na explicação. Na parte de erro, explique brevemente o erro.
    '''.format(erro_sq),
    "stream": False # Retorna toda resposta em um token
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

# print("Conteúdo da resposta:", response.text)
text = ''

data = response.json()['response'] # Retorna os dados em string

lines = data.splitlines()

ex_line = 0
# Agora, 'lines' é uma lista com cada linha do texto como um item, percorrendo essa lista, buscando pela string especifica e salvando a linha
for line in range(len(lines)):
    if lines[line] == 'Exemplo:':
        ex_line = line-1
# Formatando para puxar do texto a linha expecifica que quero e dando split onde começa o codigo
exemplo_aux = data[ex_line:].split('```')
exemplo = exemplo_aux[1][6:]

print(data)