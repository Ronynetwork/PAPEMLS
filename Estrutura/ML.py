from openai import OpenAI
import os, ast, json

options = ''
types = ''
buttons = ''
div_erros = ''


def type_erro(erro, motivo, exemplo_parts):
    type_erro = f'''
        case `{erro}`:
            return `
                <div class="solution-block">
                    <h2>{erro}</h2>
                    <h3>{motivo}</h3>
                    <pre>
                        {exemplo_parts}
                    </pre> 
                </div>
            `
    '''
    return type_erro

def option(erro, line) :
    option = f'''
                <label><input type="checkbox" value="{erro}" line="{line}" onchange="updateSolutions()">Erro: {erro}</label>
            '''
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
            <div>
                <button value="corrigir" id="actionButton" onclick="actionButton()">Corrigir</button>
                <button value="ignorar" id="actionButton" onclick="actionButton()">ignorar</button>
            </div>
        </div>
        '''

    return div_erros

try:        
    ERROR_POINT = json.dumps(os.environ["ERROR_POINT"])
    print("Erros chegando no ML: ", ERROR_POINT)
    if ERROR_POINT:
        # Buscando a API key do OpenRouter via Jenkins
        PROJECT_KEY = os.getenv("PROJECT_KEY")
        API_KEY = os.getenv("API_KEY")
        erros = ast.literal_eval(ERROR_POINT)
        for arquivo, dados in erros.items():
    
            # Dados do nome do arquivo e formatação de botão de seleção
            arq_path = arquivo.replace(f'{PROJECT_KEY}:','')
            print(f'Analisando o arquivo: {arq_path}')
            arq_name_brute = arq_path.split('/')[1] # Pega o nome do arquivo sem o caminho 
            arq_name_split = arq_name_brute.split('.')[0] # Pega o nome do arquivo sem a extensão
            extension = arq_name_brute.split('.')[1]
            button = f''' 
            <button class="fileName" id="{arq_name_brute}" value="{arq_path}" onclick="toggleShowErros('{arq_path}')"><strong>{arq_path}</strong></button>
            ''' # Botão que exibe o nome do arquivo
            buttons += button
            # --------------------------------------------------------------------------------------------------------------------------            
            

            for line, erroPure, code in dados:
                erro = erroPure.replace('"', "'")
                # print("="*100, f"Erro: {erro}, Código: {code}, linha: {line}", "="*100)

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
                        messages = [
                            {
                                "role": "user",
                                "content": f"""
                                Você é um auxiliar de correção. Sua única função é corrigir o código fornecido com base no erro indicado.

                                Regras:
                                - Mantenha exatamente a estrutura e a identação original do código.
                                - Não adicione comentários, explicações ou qualquer outro texto na área de correção.
                                - Se o erro indicar que uma função, método, variável, instrução ou linha deve ser removida, **adicione espaço vazio a linha** usando o padrão de comentário da linguagem, mantendo a identação original.
                                - Nunca apague linhas, mesmo quando o erro disser para remover algo — apenas altere para uma linha comentada.
                                - A explicação deve ser breve e aparecer apenas no campo 'Explication'.

                                Erro: {erro}  
                                Código: {code}
                                Linguagem: {extension}

                                Formato da resposta:
                                Explication: explique a correção de forma clara e rápida.
                                Correction:
                                <coloque aqui apenas o código corrigido, sem comentários, explicações ou identificação de linguagem>

                                ** Exemplo:
                                Explication: Comente a linha da variável não utilizada do código {extension}.
                                Correction:
                                // BigDecimal bd1 = BigDecimal.valueOf(d);
                                """
                            }
                        ]

                    )
                except Exception as e:
                    print("Erro ao chamar a API do OpenAI: ", e)
                    continue
                
                response = completion.choices[0].message.content # Retorna os dados em string
                # print("Conteúdo da resposta:", response.text)
                if response: 
                    data = response
                else:
                    print("reponse inexistente")
                # Agora, 'lines' é uma lista com cada linha do texto como um item. sem espaços vazios
                lines = data.splitlines()
                # Usando list compreenshion para retornar os valores necessários
                lines_filtered = [line for line in lines if line]
                if 'Correction:' in data:
                    exemplo_parts = data.split("Correction:")[1].replace('```', '') # Pega tudo que vem depois de Correction:
                else:
                    exemplo_parts = ''

                # Para a explicação final:
                if 'Explication:' in data:
                    explicationBrute= data.split("Explication:")[1].strip()
                    motivo = explicationBrute.split("Correction:")[0]

                print('Correcão sugerida:\n', exemplo_parts)
                options += option(erro, line) # Adicionando os erros à variável do html
                types += type_erro(erro, motivo, exemplo_parts) # Adicionando os erros à variável do JS
                # print('opções: ', options)
                print('types: ', types)
            # --------------------------------------------  

            # Formando div que informa o arquivo e erros
            div_erros += div_erro(arq_name_split, options)
            # --------------------------------------------
            buttons += '''
        </div>
    '''
    else:
        print("Nenhum erro encontrado no dicionário.")
except Exception as e:
    print("Erro ao processar erros do SonarQube: ", e)


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
let arqPath = ''
const errorSelect = document.getElementById("errorSelect");
const solutionDiv = document.getElementById("solution");

// lista para armazenar os erros selecionados
let selectedErrors = []; 

// Função chamada ao clicar nos botões "Corrigir" ou "Ignorar"
function actionButton() {
    const acao = document.getElementById("actionButton").value // Obtém o valor do botão clicado
    enviarAcao(acao, selectedErrors); // Chama a função para enviar a ação ao servidor
}

function toggleDropdown() {
    const checkboxes = document.getElementById("checkboxes");
    checkboxes.style.display = checkboxes.style.display === expanded ? "none" : "block";
}

// ADICIONADO FUNÇÃO PARA ESCONDER OU MOSTRAR OS ERROS DE CADA ARQUIVO
function toggleShowErros(id) {
    const id2 = id.split('.')[0];
    const idSplit = id2.split('/')[1];
    console.log('ID do arquivo clicado: ', idSplit);
    const div = document.getElementById(`erros_${idSplit}`);
    arqPath = {path: id};
    console.log(arqPath);
    
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
    console.log(checkboxes)
    const solutionDiv = document.getElementById("solution");
    selectedErrors = []; // Limpa a lista de erros selecionados

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            const path = arqPath.path; // Supondo que arqPath.path está definido
            const line = Number(checkbox.getAttribute('line'));
            const message = checkbox.value;
            const correction = getSolutionHTML(message)
                .split('<pre>')[1]
                .split('</pre>')[0]
                .replace("java", "")
                .trim();

            // Verifica se já existe um item com esse path
            let fileError = selectedErrors.find(err => err.path === path);
            if (!fileError) {
                fileError = {
                    path: path,
                    errors: []
                };
                selectedErrors.push(fileError);
            }
            console.log("fileError: ", fileError);
            console.log("selectedErrors: ", selectedErrors);
            // Adiciona o erro à lista do arquivo correspondente
            fileError.errors.push({
                line,
                message,
                correction
            });
        }
    });

    // Renderiza as soluções no HTML
    let output = "";
    selectedErrors.forEach(fileError => {
        console.log("err list: ", fileError.errors);
        fileError.errors.forEach(err => {
            output += getSolutionHTML(err.message); // Chama a função para obter o HTML da mensagem de erro identificada
        });
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
function enviarAcao(acao, errors) {
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

# print('Types:', types)
# print('Div erros:', div_erros)

html_complete = head + buttons + div_erros + body #Formatando o html completo
script = script + types + end_script # Formatando o JS completo

# print("Arquivo JS: ", script)
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