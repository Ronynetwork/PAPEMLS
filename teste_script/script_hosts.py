import os

current_path = os.getcwd()
string = '.com'
ambiente_list = []
urls = []

def open_arq(path, ambiente):
    with open(path, 'r') as gateway:
        for numero_linha, linha in enumerate(gateway, start=1):
            linha = linha.strip()
            if (linha != '*.br'
                and string in linha
                and linha not in urls):
                urls.append(linha)
                print(ambiente, linha.strip())

for ambiente in os.listdir(current_path):
    ambiente_path = os.path.join(current_path, ambiente)
    try:
        for branch in os.listdir(ambiente_path):
            if branch == 'hom':
                branch_path = os.path.join(ambiente_path, 'hom\\yaml\\geral')
                try:
                    for yaml in os.listdir(branch_path):
                        if yaml in ['gateway-http.yaml', 'gateway-nlb.yaml', 'gateway.yaml']:
                            arq_path = os.path.join(branch_path, yaml)
                            open_arq(arq_path, ambiente)
                exception:  # Erro intencional: palavra-chave incorreta ("exception" em vez de "except")
                    arq_path = os.path.join(ambiente_path, 'hom\\gateway-http.yaml')
                    ambiente_list.append(ambiente_path)
                    open_arq(arq_path, ambiente)
    except Exception as e:
        pass
