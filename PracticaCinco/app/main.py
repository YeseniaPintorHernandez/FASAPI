#1. Importaciones
from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel, Field,EmailStr
from typing import Optional, Literal
from datetime import datetime

#2. Inicializacion APP
app = FastAPI(
    title="API Biblioteca",
    description="Practica 5 Repaso",
    version="1.0.0"
    )
#BD
libros = []
prestamos = []

class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr

class Prestamo(BaseModel):
    nombre_libro: str
    usuario: Usuario

#ENDPOINTS
#Registrar libro
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):
    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail="El libro ya existe"
            )
    libros.append(libro.model_dump())
    return {
        "mensaje": "Libro registrado correctamente",
        "libro": libro
    }

#Listar libros
@app.get("/libros/")
async def listar_libros():
    disponibles = [libro for libro in libros]
    return {
        "total": len(disponibles),
        "data": disponibles
    }

#Buscar libro por nombre
@app.get("/libros/{nombre}")
async def buscar_libro(nombre: str):
    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro
    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )

#Registrar prestamo
@app.post("/prestamos/")
async def registrar_prestamo(prestamo: Prestamo):
    for libro in libros:
        if libro["nombre"].lower() == prestamo.nombre_libro.lower():
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

#Devolver libro
@app.put("/prestamos/devolver/{nombre}")
async def devolver_libro(nombre: str):
    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            if libro["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="El libro no está prestado"
                )
            libro["estado"] = "disponible"
            #Eliminar el registro del prestamo
            for index, p in enumerate(prestamos):
                if p["nombre_libro"].lower() == nombre.lower():
                    prestamos.pop(index)
                    break
            return {
                "mensaje": "Libro devuelto correctamente",
                "status": "200"
            }
    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo no existe"
    )

#Eliminar registro del prestamo
@app.delete("/prestamos/{nombre}")
async def eliminar_prestamo(nombre: str):
    for index, prestamo in enumerate(prestamos):
        if prestamo["nombre_libro"].lower() == nombre.lower():
            prestamos.pop(index)
            return {
                "mensaje": "Registro de prestamo eliminado correctamente",
                "status": "200"
            }
    raise HTTPException(
        status_code=409,
        detail="El registro de prestamo no existe"
    )