

import structlog
from fastapi import FastAPI
from redis.asyncio import Redis
from fastapi.middleware.cors import CORSMiddleware
from src.Modulos.Usuario.Usuario_router import router as usuario_router

# Configuración del logger estructurado
logger = structlog.get_logger()

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes (ajustar según sea necesario)
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
    allow_credentials=True,  # Permitir el envío de cookies y credenciales
)

app.include_router(usuario_router, prefix="/usuarios", tags=["usuarios"])