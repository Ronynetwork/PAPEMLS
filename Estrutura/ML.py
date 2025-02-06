from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': '''Erro: Specify an exception class to catch or reraise the exception
    codigo: except:


    me informe rapidamente qual sentido do aviso e uma sujestao de ajuste, retorne essas informações em tópicos que eu consiga extrar apenas as partes que quero, tipo, [SUJESTAO], [ERRO]
    ''', 
  },
])


message = response['message']['content']
erro = message.fi
print(response['message']['content'])
# or access fields directly from the response object
# print(response.message.content)