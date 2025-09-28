from openai import OpenAI
import os, ast

options = ''
types = ''
buttons = ''
div_erros = ''


def type_erro(erro, motivo, exemplo_parts):
    type_erro = '''
        case `{}`:
            return `
                <div class="solution-block">
                    <h3>{}</h3>
                    <pre>
                        {}
                    </pre> 
                </div>
            `
    '''.format(erro, erro, exemplo_parts)
    return type_erro

def option(erro) :
    option = '''
                <label><input type="checkbox" value="{}" onchange="updateSolutions()">Erro: {}</label>
            '''.format(erro, erro)
    return option

def div_erro(arq_name_split, options):

    div_erros = f'''
            <div class="erros_select" id="erros_{arq_name_split}" style="display: none;">
{options}
                <button id="selectAllButton" onclick="selectAll()">Selecionar todos</button>
                <div class="solutions">
                    <h3>Soluções:</h3>
                    <div id="solution" style="margin-top: 20px;"></div>
                </div>
            </div>
        </div>
        '''

    return div_erros

try:        
    ERROR_POINT = os.getenv("ERROR_POINT")
    print("error_point: ", ERROR_POINT)
    if ERROR_POINT:
        # Buscando a API key do OpenRouter via Jenkins
        API_KEY = os.getenv("API_KEY")
        erros = ast.literal_eval(ERROR_POINT)
        print('Print dados no arq de ML: ', erros)
        for arquivo, dados in erros.items():
    
            # Dados do nome do arquivo e formatação de botão de seleção
            arq_path = arquivo.replace(f'{os.getenv("PROJECT_KEY")}:','')
            print(f'Analisando o arquivo: {arq_path}')
            arq_name_brute = arq_path.split('/')[1]
            arq_name_split = arq_name_brute.split('.')[0]
            button = f'''
            <button class="fileName" id="{arq_name_brute}" onclick="toggleShowErros('{arq_name_split}')"><strong>{arq_path}</strong></button>
            '''
            buttons += button
            # --------------------------------------------------------------------------------------------------------------------------            
            

            for line, erro, code in dados:

                print(f"Erro: {erro}, Código: {code}, linha: {line}")
                try:
                    client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=API_KEY,
                    )

                    completion = client.chat.completions.create(
                        #   extra_headers={
                        #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                        #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
                        #   },
                        model="meta-llama/llama-3.3-8b-instruct:free",
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
                            Por favor, corrija o código abaixo com base no erro fornecido.  
                            Mantenha a estrutura e formatação original do código.

                            Erro: {erro}  
                            Código: {code}

                            Formato da resposta:
                            Explication: <explique brevemente a correção em uma linha>  
                            Correction:  
                            <coloque aqui o código corrigido>

                            Exemplo:
                            Explication: O construtor BigDecimal(double) foi substituído por BigDecimal.valueOf(double) para evitar imprecisão.  
                            Correction:  
                            BigDecimal bd1 = BigDecimal.valueOf(d);
                            """
                            }

                        ]
                    )
                except Exception as e:
                    print("Erro ao chamar a API do OpenAI: ", e)
                    continue
                
                response = completion.choices[0].message.content # Retorna os dados em string
                print('Response: \n', response)
                # print("Conteúdo da resposta:", response.text)
                if response: 
                    data = response
                else:
                    print("reponse inexistente")
                # Agora, 'lines' é uma lista com cada linha do texto como um item. sem espaços vazios
                lines = data.splitlines()
                # Usando list compreenshion para retornar os valores necessários
                lines_filtered = [line for line in lines if line]
                lines_filte_len = len(lines_filtered)
                if 'Correction:' in data:
                    exemplo_parts = data.split("Correction:")[1].replace('```', '').strip() # Pega tudo que vem depois de Correction:
                else:
                    exemplo_parts = ''

                # Para a explicação final:
                if 'Explication:' in data:
                    explicationBrute= data.split("Explication:")[1].strip()
                    motivo = explicationBrute.split("Correction:")[0].strip()

                print('='*20, 'Motivo: ', motivo, '\nExemplo parts: ', exemplo_parts, '='*20)
                options += option(erro) # Adicionando os erros à variável do html
                types += type_erro(erro, motivo, exemplo_parts) # Adicionando os erros à variável do JS
                
                # Formando div que informa o arquivo e erros
                div_erros += div_erro(arq_name_split,options)
                # --------------------------------------------
            buttons += '''
        </div>
    '''
    else:
        print("Nenhum erro encontrado no dicionário.")
except Exception as e:
    print("Erro indicado: ", e)


# Criando o arquivo html com os erros e soluções
head = '''<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Página de Erros e Soluções</title>
</head>
<body>
    <div class="container">
        <div id="header">
            <h2>Selecione o arquivo para ver seus erros</h2>
'''

body = '''
    <script src="../static/script.js"></script>
</body>
</html>
    '''

    
script = '''
let expanded = false;
const errorSelect = document.getElementById("errorSelect");
const solutionDiv = document.getElementById("solution");

function toggleDropdown() {
    const checkboxes = document.getElementById("checkboxes");
    checkboxes.style.display = checkboxes.style.display === expanded ? "none" : "block";
}

// ADICIONADO FUNÇÃO PARA ESCONDER OU MOSTRAR OS ERROS DE CADA ARQUIVO
function toggleShowErros(id) {
    const div = document.getElementById(`erros_${id}`);
    console.log(div);
    
    if (div.style.display === "none" || div.style.display === "") {
        div.style.display = "flex";
    } else {
        div.style.display = "none";
    }
}


function selectAll() {
    const checkboxes = document.querySelectorAll("input[type='checkbox']");
    const allSelected = Array.from(checkboxes).every(checkbox => checkbox.checked);

    checkboxes.forEach(checkbox => {
        checkbox.checked = !allSelected;
    });

    updateSolutions();
}

function updateSolutions() {
    const checkboxes = document.querySelectorAll("input[type='checkbox']");
    const solutionDiv = document.getElementById("solution");
    let selectedErrors = [];

    checkboxes.forEach(error => {
        if (error.checked) {
            selectedErrors.push(error.value);
            console.log(selectedErrors);
        }
        
    });

    let output = "";
    selectedErrors.forEach(error => {
        output += getSolutionHTML(error);
    });

    solutionDiv.innerHTML = output || "<p>Nenhuma solução disponível.</p>";
}
function getSolutionHTML(errorType) {
    switch (errorType) {
'''
    

end_script = '''
        default:
            return "";
    }
}
function enviarAcao(acao) {
    fetch("/receber_escolha", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "resposta": acao, "erros": errors })
    })
    .then(response => response.json())
    .then(data => alert("Escolha enviada: " + acao))
    .catch(error => console.error("Erro:", error));
}
'''

print('Types:', types)
print('Div erros:', div_erros)

html_complete = head + buttons + div_erros + body #Formatando o html completo
script = script + types + end_script # Formatando o JS completo

print("Arquivo JS: ", script)
# Cria o diretório se ele não existir
try:
    os.makedirs('./Estrutura/notification/templates', exist_ok=True)
    os.makedirs('./Estrutura/notification/static', exist_ok=True)

    with open(os.path.join('./Estrutura/notification/static', "script.js"), 'w') as static:
        static.write(script)

    with open(os.path.join('./Estrutura/notification/templates', "index.html"), 'w') as arquivo:
        arquivo.write(html_complete)

except Exception as e:
    print('Erro ao criar arquivos ', e)