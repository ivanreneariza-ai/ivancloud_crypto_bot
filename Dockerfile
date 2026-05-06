# Usar imagen oficial de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el codigo del bot
COPY . .

# Exponer el puerto que usara Flask
EXPOSE 8080

# Comando para iniciar la aplicacion
CMD ["python", "app.py"]
