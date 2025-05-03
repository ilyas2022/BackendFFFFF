import os

# Configuración de puerto dinámico
port = os.getenv("PORT", "8080")
bind = f"0.0.0.0:{port}"
workers = 4
threads = 2
worker_class = "gthread"
timeout = 120
keepalive = 5
errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'