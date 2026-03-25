# Usamos una imagen base de Python ya preparada
FROM python:3.12-slim

# Dentro del contenedor, vamos a trabajar en /app
WORKDIR /app

# Copiamos primero requirements para aprovechar la cache de Docker
COPY requirements.txt .

# Instalamos dependencias dentro de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente al contenedor
COPY app ./app

# Cuando arranque el contenedor, ejecutará uvicorn
# --host 0.0.0.0 es clave para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000", "--reload"]