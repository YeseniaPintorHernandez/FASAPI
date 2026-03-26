#1. importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios
from app.data.db import engine
from app.data import usuario


usuario.Base.metadata.create_all(bind=engine)

#**********************
#2. Inicializaciones APP
#**********************
app= FastAPI(
    title=' Mi Primer API ',
    description="Yesenia Pintor Hernández",
    version= '1.0.0'
            )
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
