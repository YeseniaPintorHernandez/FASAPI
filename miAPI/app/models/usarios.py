from pydantic import BaseModel,Field
#Creamos un modelo de datos
class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usuario") #Los tres puntos quiere decir obligatorio y gt=0 que debe ser mayor a 0
    nombre:str = Field(..., min_length=3,max_length=50,example="Juanita")#minimo tres carcateres maximo 50
    edad:int = Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")#minimo 1 año maximo 123 años