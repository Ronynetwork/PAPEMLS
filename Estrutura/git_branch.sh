#!/bin/bash
# Define o repositório remoto (com HTTPS ou SSH, escolha uma)
git remote set-url origin git@github.com:Ronynetwork/PAPEMLS.git

# Garante que está na branch 'dev'
git checkout dev || exit 1

# Atualiza a branch local com a versão remota usando rebase
git reset --hard
git pull origin dev --rebase || {
  echo "Erro ao fazer rebase. Corrija os conflitos e tente novamente."
  exit 1
}

# Adiciona arquivos modificados no diretório teste_script/
git add ./teste_script/

# Verifica se há mudanças para commitar
if git diff --cached --quiet; then
  echo "Nenhuma alteração para commitar."
else
  # Faz o commit com a mensagem padrão
  git commit -m "FIX: Correction commit"
  
  # Tenta fazer o push para o repositório remoto
  git push origin dev || {
    echo "Erro ao fazer push. Verifique o estado da branch remota."
    exit 1
  }
fi
