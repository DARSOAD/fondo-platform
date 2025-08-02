# Imagen base
FROM python:3.10-slim

# Variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar curl
RUN apt-get update && apt-get install -y curl

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Dar permisos al script de entrada
RUN chmod +x /app/entrypoint.sh

# Usar entrypoint personalizado
ENTRYPOINT ["/app/entrypoint.sh"]
