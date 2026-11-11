# Imagen base oficial de Python ligera
FROM python:3.11-slim

# Metadatos del proyecto
LABEL autor="Evelyn Cerro"
LABEL descripcion="Contenedor de ejecucion para el flujo DevOps de extraccion y publicacion"

# Establecer directorio de trabajo en el contenedor
WORKDIR /aplicacion

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente y carpetas de soporte
COPY modulos/ ./modulos/
COPY datos/ ./datos/
COPY principal.py .

# Ejecutar el flujo de extraccion y generacion de artefactos
RUN python principal.py

# Exponer el puerto para servir el dashboard
EXPOSE 8080

# Comando para servir la carpeta dist con el servidor HTTP nativo
CMD ["python", "-m", "http.server", "8080", "--directory", "dist"]
