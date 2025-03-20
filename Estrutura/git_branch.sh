#!/bin/bash
# Configurar o Git para usar o token
git config --global user.email "ronyldooliveira16@gmail.com"
git config --global user.name "Ronynetwork"
git remote set-url origin https://$GIT_USER:$GIT_TOKEN@github.com/Ronynetwork/PAPEMLS.git

# Conferindo se a branch main existe, se não, cria
git checkout -b main || git checkout main
git pull origin main

# Adicionar apenas o arquivo desejado
git add ./teste_script/script_hosts.py
git restore .

# Fazer o commit com uma mensagem
git commit -m "Correction commit"

# Enviar as mudanças para o repositório remoto
git push origin main
