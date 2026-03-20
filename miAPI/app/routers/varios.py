from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(tags=['Inicio'])

#**********************
#3.Endpoints
#**********************
@routerV.get("/")
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@routerV.get("/v1/bienvenidos")
async def holaMundo():
    return {"mensaje":"Bienvenidos"}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(3) #simulacion, peticion, cunsultaBD...
    return {
        "Calificacion":"7.5",
        "estatus":"200"
        }

@routerV.get("/v1/usuario/{id}") #El id es un parametro de ruta
async def consultauno(id:int):
    await asyncio.sleep(3)
    return {
    "Resultado":"usuario encontrado",
    "Estatus":"200"
    }

@routerV.get("/v1/usuarios_op/")
async def consultaOp(id:Optional[int]=None):#Que es un parametro opcional
    await asyncio.sleep(2)
    if id is not None: #Si si enviaron el id
        for usuario in usuarios:#Recorre todos los usuarios
            if usuario ["id"] == id: #compara para buscar el usuario
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return{"Aviso":"No se proporciono Id"}

