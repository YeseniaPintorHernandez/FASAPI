#1. importaciones
from fastapi import FastAPI,status,HTTPException,Depends
from typing import Optional
import asyncio
from pydantic import BaseModel,Field
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#**********************
#2. Inicializaciones APP
#**********************
app= FastAPI(
    title=' Mi Primer API ',
    description="Yesenia Pintor Hernández",
    version= '1.0.0'
             )

SECRET_KEY = "mi_clave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
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


#VALIDAR TOKEN
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
#**********************
#3.Endpoints
#**********************
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if username != "yeseniap" or password != "123456":
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token({"sub": username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


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
                status_code=401,
                detail=" El id ya existe"
            )
    usuarios.append(usuario.dict())# si no existe se agrega a la lista
    return{
        "mensaje":"usuario agregado",
        "usuario":usuario
    }

#**********************
#Endpoint Tipo PUT
#**********************
@app.put("/v1/usuarios/", tags=['CRUD_HTTP'])
async def actualiza_usuario(usuario: crear_usuario, user: str = Depends(verificar_token)):
    for index, usr in enumerate(usuarios):#recorre los usuarios, el enumerate devuelve indice y valor
        if usr["id"] == usuario["id"]:
            usuarios[index] = usuario #si encunetra el usuario lo reemplaza
            return {
                "mensaje": "usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario
            }
    raise HTTPException(
        status_code=401,
        detail="usuario no encontrado"
    )
#**********************
#Endpoint Tipo DELETE
#**********************
@app.delete("/v1/usuarios/", tags=['CRUD_HTTP'])
async def elimina_usuario(id: int, user: str = Depends(verificar_token)): #el parametro es id pero tiene seguridad con estouserAuth:str=Depends(verificar_peticion
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index) # elimina el usuario de la lista
            return {
                "mensaje": f"usuario eliminado por {user}",
                "status": "200",
                "usuario": usuario_eliminado
            }
    raise HTTPException(
        status_code=401,
        detail="usuario no encontrado"
    )