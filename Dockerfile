FROM python:3.12-slim

# Evita .pyc y asegura logs sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Trabajaremos en /app (después cambiaremos de dir según el proyecto)
WORKDIR /app

# Dependencias del sistema para compilar paquetes de Python (mysqlclient, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python primero (mejor caché)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia TODO tu repo (helloworld/, todoapp/, etc.) dentro de /app
COPY . /app

# Variables para seleccionar qué proyecto correrás (helloworld o todoapp).
# Las puedes sobreescribir al ejecutar el contenedor o con --env-file.
ENV PROJECT_DIR=helloworld \
    WSGI_MODULE=helloworld_project.wsgi

EXPOSE 8000

# Ejecuta Gunicorn apuntando al módulo WSGI y cambiando de dir al proyecto elegido
CMD ["sh","-lc","gunicorn ${WSGI_MODULE}:application --chdir ${PROJECT_DIR} --bind 0.0.0.0:8000 --workers 3"]
