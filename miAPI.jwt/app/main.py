#1. importaciones
from fastapi import FastAPI,status,HTTPException,Depends
from typing import Optional
import asyncio
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#**********************
#2. Inicializaciones APP
#**********************
app= FastAPI(
    title=' Mi Primer API ',
    description="Yesenia Pintor Hernández",
    version= '1.0.0'
             )
#**********************
#BD ficticia 
#**********************
usuarios=[
    {"id":1,"nombre":"Yesenia","edad":23},
    {"id":2,"nombre":"Fernanda","edad":20},
    {"id":3,"nombre":"Benjamin","edad":20},
]
#Creamos un modelo de datos
class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usuario") #Los tres puntos quiere decir obligatorio y gt=0 que debe ser mayor a 0
    nombre:str = Field(..., min_length=3,max_length=50,example="Juanita")#minimo tres carcateres maximo 50
    edad:int = Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")#minimo 1 año maximo 123 años

#**********************
#Seguridad HTTP BASIC
#**********************

seguridad= HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)): #Se obtiene usuario y contraseña
    userAuth= secrets.compare_digest(credenciales.username,"yeseniap")#compara el usuario
    passAuth= secrets.compare_digest(credenciales.password,"123456")#compara la contraseña

    if not(userAuth and passAuth ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,#Si esta mal devulve ese mensaje y error 401
            detail="Credenciales no Autorizadas"
        )
    return credenciales.username #devuelve el usuario ya autenticado

#**********************
#3.Endpoints
#**********************
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

@app.get("/v1/usuario/{id}", tags=['Parametros']) #El id es un parametro de ruta
async def consultauno(id:int):
    await asyncio.sleep(3)
    return {
    "Resultado":"usuario encontrado",
    "Estatus":"200"
    }

@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):#Que es un parametro opcional
    await asyncio.sleep(2)
    if id is not None: #Si si enviaron el id
        for usuario in usuarios:#Recorre todos los usuarios
            if usuario ["id"] == id: #compara para buscar el usuario
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return{"Aviso":"No se proporciono Id"}

#**********************
# Endpoint Tipo GET   
#**********************
@app.get("/v1/usuarios/", tags=['CRUD_HTTP'])#Devuelve el total de usuarios y la lista
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
#**********************
#Endpoint Tipo post
#**********************
@app.post("/v1/usuarios/", tags=['CRUD_HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:#validacion de ID duplicado 
            raise HTTPException(#si el id existe
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario)# si no existe se agrega a la lista
    return{
        "mensaje":"usuario agregado",
        "usuario":usuario
    }

#**********************
#Endpoint Tipo PUT
#**********************
@app.put("/v1/usuarios/", tags=['CRUD_HTTP'])
async def actualiza_usuario(usuario:dict):
    for index, usr in enumerate(usuarios):#recorre los usuarios, el enumerate devuelve indice y valor
        if usr["id"] == usuario["id"]:
            usuarios[index] = usuario #si encunetra el usuario lo reemplaza
            return {
                "mensaje": "usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=400,
        detail="usuario no encontrado"
    )
#**********************
#Endpoint Tipo DELETE
#**********************
@app.delete("/v1/usuarios/", tags=['CRUD_HTTP'])
async def elimina_usuario(id: int,userAuth:str=Depends(verificar_peticion)): #el parametro es id pero tiene seguridad con estouserAuth:str=Depends(verificar_peticion
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index) # elimina el usuario de la lista
            return {
                "mensaje": f"usuario eliminado por {userAuth} ",
                "status": "200",
                "usuario": usuario_eliminado
            }
    raise HTTPException(
        status_code=400,
        detail="usuario no encontrado"
    )