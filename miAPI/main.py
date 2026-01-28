#1. importaciones
from fastapi import FastAPI

#2. Inicializaciones APP
app= FastAPI()

#3.Endpoints
@app.get("/")
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("/bienvenidos")
async def holaMundo():
    return {"mensaje":"Bienvenidos"}