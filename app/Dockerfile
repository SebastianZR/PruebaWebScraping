# Usar una imagen base optimizada de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias necesarias y Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo requirements.txt antes de instalar
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y sqlite3

# Copiar el código de la aplicación
COPY . .

# Comando para ejecutar el script principal
CMD ["python", "WebScraping.py"]