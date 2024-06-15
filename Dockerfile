# Usa una imagen base oficial de Python
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0


# Copia los archivos de Poetry y el archivo de configuración
COPY pyproject.toml poetry.lock ./

# Instala Poetry
RUN pip install poetry

# Instala las dependencias del proyecto
RUN poetry install --no-root

# Copia todo el contenido del proyecto en el contenedor
COPY . .

# Expone el puerto que el servidor de Django usará
EXPOSE 8000

# Define el comando predeterminado para ejecutar cuando el contenedor se inicie
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
