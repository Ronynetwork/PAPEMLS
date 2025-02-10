import requests, json

url = 'http://localhost:10012/api/generate'

erro_sq = 'Specify an exception class to catch or reraise the exception'

data = {
    "model": "llama3.2:1b", 
    "prompt": '''Erro: {}
    codigo: 'except:'
    me informe rapidamente descrição breve do motivo do e um exemplo.
    cite apenas um exemplo na explicação. Na parte de erro, explique brevemente o erro mas nao cite exemplos.
    '''.format(erro_sq),
    "max_tokens": 50,
    "stream": True
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

# print("Conteúdo da resposta:", response.text)
text = ''

lines = response.text.strip().split("\n")  # Divide em linhas
for line in lines:
    json_data = json.loads(line) # Converte cada linha em JSON
    text += json_data['response']
    if json_data['response'] == 'Exemplo':
        print('exemplo na linha', line)
        exemplo_line = line

exemplo = text[exemplo_line:]

print(exemplo)