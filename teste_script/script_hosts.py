import os

# ❌ ERRO: Credenciais fixas no código (Hardcoded Credentials)
DB_USER = "admin"
DB_PASSWORD = "senha123"  # SonarQube deve detectar isso como um problema de segurança

def conectar_banco():
    # Simulação de uma conexão insegura ao banco de dados
    conexao = f"mysql://{DB_USER}:{DB_PASSWORD}@localhost/meubanco"
    print(f"Conectando ao banco com: {conexao}")  # ❌ Isso vaza credenciais no log!

    return conexao

if __name__ == "__main__":
    conectar_banco()
