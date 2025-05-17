FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiamos solo el archivo de requisitos primero para aprovechar la cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Creamos carpetas requeridas por Flask y movemos los archivos manualmente
RUN mkdir -p web/templates web/static && \
    cp web/index.html web/templates/index.html && \
    cp web/styles.css web/static/styles.css

CMD ["python", "app.py"]
