#importamos la imagen base de python
FROM python:3.12-slim

#Crear Carpeta de trabajo
WORKDIR /app

#copiar requerimientos
COPY requirements.txt .

#Instalar requerimientos
RUN pip install --no-cache-dir -r requirements.txt

#copiar archivo dell API
COPY ./app ./app

#Exponer puerto
EXPOSE 5000

#Comando para ejecutar FASTAPI
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","5000","--reload"]