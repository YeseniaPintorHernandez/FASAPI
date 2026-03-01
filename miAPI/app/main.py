#1. importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel,Field

#2. Inicializaciones APP
app= FastAPI(
    title=' Mi Primer API ',
    description="Yesenia Pintor Hernández",
    version= '1.0.0'
             )

#BD ficticia 
usuarios=[
    {"id":1,"nombre":"Yesenia","edad":23},
    {"id":2,"nombre":"Fernanda","edad":20},
    {"id":3,"nombre":"Benjamin","edad":20},
]

class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str = Field(..., min_length=3,max_length=50,example="Juanita")
    edad:int = Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")

#3.Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) #simulacion, peticion, cunsultaBD...
    return {
        "Calificacion":"7.5",
        "estatus":"200"
        }

@app.get("/v1/usuario/{id}", tags=['Parametros'])
async def consultauno(id:int):
    await asyncio.sleep(3)
    return {
    "Resultado":"usuario encontrado",
    "Estatus":"200"
    }

@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario ["id"] == id:
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return{"Aviso":"No se proporciono Id"}
#
# Endpoint Tipo GET   
@app.get("/v1/usuarios/", tags=['CRUD_HTTP'])
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }

#Endpoint Tipo post
@app.post("/v1/usuarios/", tags=['CRUD_HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado",
        "usuario":usuario
    }

#Endpoint Tipo PUT
@app.put("/v1/usuarios/", tags=['CRUD_HTTP'])
async def actualiza_usuario(usuario:dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario["id"]:
            usuarios[index] = usuario
            return {
                "mensaje": "usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=400,
        detail="usuario no encontrado"
    )

#Endpoint Tipo DELETE
@app.delete("/v1/usuarios/", tags=['CRUD_HTTP'])
async def elimina_usuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {
                "mensaje": "usuario eliminado correctamente",
                "status": "200",
                "usuario": usuario_eliminado
            }
    raise HTTPException(
        status_code=400,
        detail="usuario no encontrado"
    )