#!/bin/bash

# Cria o ambiente virtual
python3 -m venv papemls

# Ativa o ambiente virtual
source papemls/bin/activate

# Instala as dependências do arquivo requirements.txt
pip install install flask requests os
