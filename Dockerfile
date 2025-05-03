#Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorio para uploads si no existe
RUN mkdir -p uploads && chmod 777 uploads


# Puerto
EXPOSE ${PORT}

# Comando para producción usando Gunicorn
CMD sh -c "gunicorn --config gunicorn_config.py --bind 0.0.0.0:${PORT} app:app"

