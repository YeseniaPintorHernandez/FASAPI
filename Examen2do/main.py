from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel, Field,EmailStr
from typing import Optional, Literal
from datetime import datetime

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
    estado: Literal["sencilla", "doble","suite"]

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

#Listar reservas
@app.get("/reservas/")
async def listar_reservas():
    disponibles = [reserva for reserva in reservas]
    return {
        "total": len(disponibles),
        "data": disponibles
    }

#Buscar reserva por id
@app.get("/reservaciones/{id}")
async def buscar_libro(id: int):
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
    for libro in reservaciones:
        if libro["nombre"].lower() == reservacion.nombre_huesped.lower():
            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )
            libro["estado"] = "prestado"
            prestamos.append(prestamo.model_dump())
            return {
                "mensaje": "Prestamo registrado correctamente",
                "libro": libro["nombre"],
                "Nombre de la persona": prestamo.usuario.nombre
            }
    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )
