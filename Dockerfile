# Usamos una versión ligera de Python
FROM python:3.9-slim

# Evita que Python guarde archivos .pyc y fuerza que los logs salgan rápido
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos las librerías necesarias
COPY requirements.txt .

# Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo tu código dentro del contenedor
COPY . .

# Variable clave para que el script sepa que está en Docker
ENV AM_I_IN_DOCKER="True"

# El comando que se ejecuta al arrancar: Lanza el scheduler
CMD ["python", "src/scheduler.py"]