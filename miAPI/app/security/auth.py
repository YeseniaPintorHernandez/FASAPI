from fastapi import status,HTTPException,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
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
