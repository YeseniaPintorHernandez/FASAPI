from fastapi import FastAPI,HTTPException,status,Depends
from pydantic import BaseModel, Field,EmailStr
from typing import Optional, Literal
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#2. Inicializacion APP
app = FastAPI(
    title="API Reservas Hospedaje",
    description="Examen",
    version="1.0.0"
    )

#BD
huesped = []
reservas = []

class huesped(BaseModel):
    nombre: str
    correo: EmailStr

class reservas(BaseModel):
    usuario: huesped
    dia_entrada: int = Field(..., gt=8)
    mes_entrada: int = Field(..., gt=3)
    año_entrada: int = Field(..., gt=2026)
    dia_salida: int = Field(..., gt=9)
    mes_salida: int = Field(..., gt=3)
    año_salida: int = Field(..., gt=2026)
    tipo_habitacion: Literal["sencilla", "doble","suite"]

#**********************
#Seguridad HTTP BASIC
#**********************

seguridad= HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth= secrets.compare_digest(credenciales.username,"hotel")
    passAuth= secrets.compare_digest(credenciales.password,"r2026")

    if not(userAuth and passAuth ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    return credenciales.username

#Registrar huesped
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
async def registrar_huesped(huesped: huesped):
    for l in huespedes:
        if l["nombre"].lower() == huesped.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail="El huesped ya existe"
            )
    huespedes.append(huesped.model_dump())
    return {
        "mensaje": "huesped registrado correctamente",
        "huesped": huesped
    }

#Listar reservaciones
@app.get("/reservaciones/")
async def listar_reservas():
    disponibles = [reserva for reserva in reservaciones]
    return {
        "total": len(disponibles),
        "data": disponibles
    }

#Buscar reservacion por id
@app.get("/reservaciones/{id}")
async def buscar_reservacion(id: int):
    for reservacion in reservaciones:
        if index["id"]:
            return reservacion
    raise HTTPException(
        status_code=400,
        detail="reservacion no encontrada"
    )

#Crear reservacion
@app.post("/reservaciones/")
async def registrar_reservacion(reservacion: reservacion):
    for reservacion in tipo_habitacion:
        if tipo_habitacion ["sencilla", "doble","suite"] == tipo_habitacion.nombre_reservacion.lower():
            if reservacion["tipo_habitacion"] == "sencilla"or "doble"or"suite":
                raise HTTPException(
                    status_code=409,
                    detail="Ese tipo de habitacion no esxiste"
                )
            reservacion["tipo_habitacion"] = "reservado"
            reservaciones.append(reservacion.model_dump())
            return {
                "mensaje": "Reservacion registrado correctamente",
                "Nombre de la persona": reservacion.usuario.nombre
            }
    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )

#Cancelar reservacion
@app.put("/reservaciones/cancelar/{id}")
async def cnacelar_reservaciones(id: int,userAuth:str=Depends(verificar_peticion)):
    for index, reservaciones in enumerate(reservaciones):
        if reservaciones["id"] == id:
            if reserva["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="la habitacion ya no esta reservada"
                )
            reservacion["estado"] = "disponible"
            #Eliminar el registro de la reservacion
            for index, p in enumerate(reservaciones):
                if p["nombre_libro"].lower() == nombre.lower():
                    reservaciones.pop(index)
                    break
            return {
                "mensaje": "usuario eliminado correctamente",
                "mensaje": f"usuario eliminado por {userAuth} ",
                "status": "200",
                "usuario": reservacion_cancelada
            }
    raise HTTPException(
        status_code=409,
        detail="La reservacion no existe"
    )