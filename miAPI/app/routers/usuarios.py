#**********************
# CRUD Usuarios   
#**********************
from fastapi import status,HTTPException,Depends,APIRouter
from app.data.database import usuarios
from app.models.usarios import crear_usuario
from app.security.auth import verificar_peticion


from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD_HTTP']

)
#**********************
# Endpoint Tipo GET   
#**********************
@routerU.get("/")#Devuelve el total de usuarios y la lista
async def leer_usuario(db:Session= Depends(get_db)):

    queryUsuarios= db.query(usuarioDB).all()
    return{
        "status":"200",
        "total": len(queryUsuarios),
        "usuarios":queryUsuarios
    }
#**********************
#Endpoint Tipo post
#**********************
@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:crear_usuario, db:Session= Depends(get_db)):
    usuarioNuevo= usuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    return{
        "mensaje":"usuario agregado",
        "usuario":usuarioP
    }

#**********************
#Endpoint Tipo PUT
#**********************
@routerU.put("/")
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
@routerU.delete("/")
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