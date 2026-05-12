from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .Usuario_schema import UsuarioCreate, UsuarioRead
from .Usuario_service import UsuarioService
import src.database as database

router = APIRouter()

@router.post("/registro", response_model=UsuarioRead)
async def registrar_usuario(datos: UsuarioCreate, db: AsyncSession = Depends(database.get_db)):
    service = UsuarioService(db)

    return await service.crear_usuario(datos)