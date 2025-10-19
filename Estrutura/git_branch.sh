#!/bin/bash
# Configurar o Git para usar o token
git remote set-url origin git@github.com:Ronynetwork/PAPEMLS.git

# Conferindo se a branch main existe, se não, cria
git checkout dev
git pull origin dev --rebase

# Adicionar apenas o arquivo desejado
git add ./teste_script/
git restore .

# Fazer o commit com uma mensagem
git commit -m "FIX: Correction commit"

# Enviar as mudanças para o repositório remoto
git push origin dev
