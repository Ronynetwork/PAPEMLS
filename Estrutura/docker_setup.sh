#!/bin/sh

# Atualiza a lista de pacotes e instala dependências necessárias
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Cria o diretório para armazenar a chave GPG do Docker
sudo install -m 0755 -d /etc/apt/keyrings

# Baixa a chave GPG do Docker e altera as permissões
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Adiciona o repositório Docker às fontes do Apt
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualiza a lista de pacotes e instala o Latest dos plugins docker
VERSION_DOCKER=5:27.4.0-1~ubuntu.24.04~noble
sudo apt-get update
sudo apt-get install -y docker-ce=$VERSION_DOCKER docker-ce-cli=$VERSION_DOCKER containerd.io docker-buildx-plugin docker-compose-plugin
