#!/bin/bash
# Script para iniciar o servidor Gunicorn em produção
# Uso: ./gunicorn_start.sh

# Ativar ambiente virtual (se existir)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Definir variáveis de ambiente (ajuste conforme necessário)
export FLASK_APP=server.py
export LOG_LEVEL=INFO
export LOG_DIR=logs
export UPLOAD_FOLDER=/tmp/uploads

# Criar diretórios necessários
mkdir -p logs
mkdir -p /tmp/uploads

# Iniciar Gunicorn
exec gunicorn -c gunicorn_config.py server:app
