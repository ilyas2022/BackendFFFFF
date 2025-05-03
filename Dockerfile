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

# Variables de entorno
ENV REPLICATE_API_TOKEN=r8_7IfUadQSkl3N2PGZR4HWswF3J55FUfZ0TUiQj
ENV CLOUDINARY_CLOUD_NAME=dbgwyc5o4
ENV CLOUDINARY_API_KEY=873135915466665
ENV CLOUDINARY_API_SECRET=uptiwp7Chfu1Z0SkUaC-iHaSVUE
ENV ALLOWED_ORIGINS=*
ENV PYTHONUNBUFFERED=1

# Puerto
EXPOSE 5000

# Comando para producción usando Gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "--bind", "0.0.0.0:5000", "app:app"]