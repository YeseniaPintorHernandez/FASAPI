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
libros = []#Crea una lista vacía, esta lista almacenará todos los libros registrados
prestamos = []#Lo mismo pero con los prestamos

class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int = Field(..., gt=1450, le=datetime.now().year)# debe ser entero, mayor que 1450, menor o igual al año actual
    paginas: int = Field(..., gt=1)#mínimo 2 páginas
    estado: Literal["disponible", "prestado"] = "disponible"#Define el estado del libro pero es disponidle predeterminadamente

class Usuario(BaseModel):#Modelo de datos para un usuario
    nombre: str
    correo: EmailStr#Correo validado automáticamente

#Modelo que representa un préstamo
class Prestamo(BaseModel):
    nombre_libro: str
    usuario: Usuario #Dentro del préstamo vendrá un objeto usuario, por ejemplo los datos que pide el prestamo

#ENDPOINTS
#Registrar libro
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: Libro):#Recibe un objeto libro que debe cumplir el modelo Librov                 
    for l in libros:#Recorre todos los libros registrados
        if l["nombre"].lower() == libro.nombre.lower():#Compara nombres .lower() convierte todo a minúsculas
            raise HTTPException(
                status_code=400,
                detail="El libro ya existe"
            )
    libros.append(libro.model_dump()) #model_dump() convierte el modelo Pydantic en diccionario,luego se guarda en la lista
    return {
        "mensaje": "Libro registrado correctamente",
        "libro": libro
    }

#Listar libros
@app.get("/libros/")
async def listar_libros():
    disponibles = [libro for libro in libros] #crear una lista con todos los libros
    return {
        "total": len(disponibles),#Cuenta cuántos libros hay
        "data": disponibles#Devuelve todos los libros
    }

#Buscar libro por nombre
@app.get("/libros/{nombre}")
async def buscar_libro(nombre: str):
    for libro in libros:#Recorre todos los libros
        if libro["nombre"].lower() == nombre.lower():#Busca el libro
            return libro
    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )

#Registrar prestamo
@app.post("/prestamos/")
async def registrar_prestamo(prestamo: Prestamo):#Recibe datos del préstamo
    for libro in libros:#Busca el libro
        if libro["nombre"].lower() == prestamo.nombre_libro.lower():#Compara nombres
            if libro["estado"] == "prestado":#Verifica si el libro ya está prestado
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )
            libro["estado"] = "prestado"#Cambia el estado del libro
            prestamos.append(prestamo.model_dump())#Guarda el préstamo en la lista
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
    for libro in libros:#Busca el libro
        if libro["nombre"].lower() == nombre.lower():
            if libro["estado"] == "disponible":#Verifica si el libro ya está disponible
                raise HTTPException(
                    status_code=409,
                    detail="El libro no está prestado"
                )
            libro["estado"] = "disponible"#Marca el libro como disponible
            #Eliminar el registro del prestamo
            for index, p in enumerate(prestamos):#Recorre los préstamos
                if p["nombre_libro"].lower() == nombre.lower():
                    prestamos.pop(index)#Elimina el préstamo
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
    for index, prestamo in enumerate(prestamos):#Recorre todos los préstamos
        if prestamo["nombre_libro"].lower() == nombre.lower():#Busca el préstamo del libro
            prestamos.pop(index)#Elimina el préstamo
            return {
                "mensaje": "Registro de prestamo eliminado correctamente",
                "status": "200"
            }
    raise HTTPException(
        status_code=409,
        detail="El registro de prestamo no existe"
    )