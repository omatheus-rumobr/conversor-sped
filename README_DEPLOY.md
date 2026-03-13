# Guia de Deploy - Digital Ocean

Este guia explica como fazer o deploy do microsserviço Flask usando Gunicorn no Digital Ocean.

## Pré-requisitos

- Servidor Ubuntu/Debian no Digital Ocean
- Python 3.8+ instalado
- Acesso SSH ao servidor

## Passo a Passo

### 1. Conectar ao servidor

```bash
ssh root@seu-ip-digital-ocean
```

### 2. Atualizar o sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Instalar Python e dependências

```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 4. Criar usuário para a aplicação (recomendado)

```bash
sudo adduser --disabled-password --gecos "" appuser
sudo su - appuser
```

### 5. Clonar ou fazer upload do código

```bash
# Se usar Git
git clone seu-repositorio.git
cd conversorSPEDS

# Ou fazer upload via SCP do seu computador local
```

### 6. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 7. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 8. Configurar variáveis de ambiente

Crie um arquivo `.env` ou exporte as variáveis:

```bash
export FLASK_APP=server.py
export LOG_LEVEL=INFO
export LOG_DIR=/home/appuser/logs
export UPLOAD_FOLDER=/home/appuser/uploads
export PORT=8000
```

### 9. Criar diretórios necessários

```bash
mkdir -p logs
mkdir -p uploads
```

### 10. Testar a aplicação localmente

```bash
python server.py
```

### 11. Iniciar com Gunicorn

#### Opção A: Executar diretamente

```bash
gunicorn -c gunicorn_config.py server:app
```

#### Opção B: Usar o script de inicialização

```bash
chmod +x gunicorn_start.sh
./gunicorn_start.sh
```

#### Opção C: Usar systemd (recomendado para produção)

Crie o arquivo `/etc/systemd/system/conversor-sped.service`:

```ini
[Unit]
Description=Conversor SPED Gunicorn daemon
After=network.target

[Service]
User=appuser
Group=appuser
WorkingDirectory=/home/appuser/conversorSPEDS
Environment="PATH=/home/appuser/conversorSPEDS/venv/bin"
Environment="FLASK_APP=server.py"
Environment="LOG_LEVEL=INFO"
Environment="LOG_DIR=/home/appuser/logs"
Environment="UPLOAD_FOLDER=/home/appuser/uploads"
ExecStart=/home/appuser/conversorSPEDS/venv/bin/gunicorn -c gunicorn_config.py server:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ativar e iniciar o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable conversor-sped
sudo systemctl start conversor-sped
sudo systemctl status conversor-sped
```

### 12. Configurar Nginx (opcional, mas recomendado)

Instalar Nginx:

```bash
sudo apt install nginx -y
```

Criar arquivo de configuração `/etc/nginx/sites-available/conversor-sped`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com ou seu-ip;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```

Ativar o site:

```bash
sudo ln -s /etc/nginx/sites-available/conversor-sped /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 13. Configurar firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Comandos Úteis

### Ver logs da aplicação

```bash
# Logs do Gunicorn
sudo journalctl -u conversor-sped -f

# Logs da aplicação (Loguru)
tail -f logs/app_*.log
```

### Reiniciar o serviço

```bash
sudo systemctl restart conversor-sped
```

### Parar o serviço

```bash
sudo systemctl stop conversor-sped
```

### Ver status

```bash
sudo systemctl status conversor-sped
```

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `FLASK_APP` | Nome do arquivo da aplicação | `server.py` |
| `LOG_LEVEL` | Nível de log (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `LOG_DIR` | Diretório para salvar logs | `logs` |
| `UPLOAD_FOLDER` | Diretório para uploads temporários | `/tmp` |
| `PORT` | Porta para desenvolvimento | `5000` |
| `GUNICORN_BIND` | Endereço e porta do Gunicorn | `0.0.0.0:8000` |
| `GUNICORN_WORKERS` | Número de workers | `CPU * 2 + 1` |
| `GUNICORN_TIMEOUT` | Timeout em segundos | `120` |

## Troubleshooting

### Aplicação não inicia

1. Verificar logs: `sudo journalctl -u conversor-sped -n 50`
2. Verificar se a porta está em uso: `sudo netstat -tulpn | grep 8000`
3. Verificar permissões dos diretórios

### Erro de permissão

```bash
sudo chown -R appuser:appuser /home/appuser/conversorSPEDS
```

### Aplicação muito lenta

Ajustar número de workers no `gunicorn_config.py` ou variável `GUNICORN_WORKERS`

## Monitoramento

- Health check: `http://seu-ip/health`
- Swagger: `http://seu-ip/swagger`
