"""
Configuração do Gunicorn para produção
"""
import os
import multiprocessing

# Configurações do servidor
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', 1000))
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 5))

# Configurações de performance
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 50))
preload_app = os.getenv('GUNICORN_PRELOAD_APP', 'True').lower() == 'true'

# Configurações de logging
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '-')  # '-' = stdout
errorlog = os.getenv('GUNICORN_ERROR_LOG', '-')    # '-' = stderr
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configurações de segurança
limit_request_line = int(os.getenv('GUNICORN_LIMIT_REQUEST_LINE', 4094))
limit_request_fields = int(os.getenv('GUNICORN_LIMIT_REQUEST_FIELDS', 100))
limit_request_field_size = int(os.getenv('GUNICORN_LIMIT_REQUEST_FIELD_SIZE', 8190))

# Configurações de processo
daemon = os.getenv('GUNICORN_DAEMON', 'False').lower() == 'true'
pidfile = os.getenv('GUNICORN_PIDFILE', None)
user = os.getenv('GUNICORN_USER', None)
group = os.getenv('GUNICORN_GROUP', None)
tmp_upload_dir = os.getenv('GUNICORN_TMP_UPLOAD_DIR', None)

# Configurações de threads (se usar worker_class='gthread')
threads = int(os.getenv('GUNICORN_THREADS', 1))

# Hooks
def on_starting(server):
    """Executado quando o Gunicorn inicia"""
    server.log.info("Iniciando servidor Gunicorn...")

def on_reload(server):
    """Executado quando o Gunicorn recarrega"""
    server.log.info("Recarregando servidor Gunicorn...")

def worker_int(worker):
    """Executado quando um worker recebe SIGINT ou SIGQUIT"""
    worker.log.info("Worker recebeu sinal de interrupção")

def pre_fork(server, worker):
    """Executado antes de criar um worker"""
    pass

def post_fork(server, worker):
    """Executado depois de criar um worker"""
    server.log.info(f"Worker {worker.pid} criado")

def post_worker_init(worker):
    """Executado depois que o worker inicializa a aplicação"""
    worker.log.info(f"Worker {worker.pid} inicializado")

def worker_abort(worker):
    """Executado quando um worker aborta"""
    worker.log.info(f"Worker {worker.pid} abortado")
