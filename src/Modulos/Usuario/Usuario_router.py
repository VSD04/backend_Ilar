from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .Usuario_schema import UsuarioCreate, UsuarioLogin, UsuarioRead
from .Usuario_service import UsuarioService
import src.database as database

router = APIRouter()

@router.post("/registro", response_model=UsuarioRead)
async def registrar_usuario(datos: UsuarioCreate, db: AsyncSession = Depends(database.get_db)):
    service = UsuarioService(db)

    return await service.crear_usuario(datos)

@router.get("/all", response_model=list[UsuarioRead])
async def listar_usuarios(db: AsyncSession = Depends(database.get_db)):
    service = UsuarioService(db)
    listar_usuarios = await service.listar_todos()
    return listar_usuarios

@router.post("/login")
async def inicio_sesion(datos: UsuarioLogin, db: AsyncSession = Depends(database.get_db)):
    service = UsuarioService(db)
    usuario = await service.login_usuario(datos)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return  {"message" : "Login exitoso", "Usuario #": usuario.id}


@router.get("/{usuario_id}", response_model=UsuarioRead)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(database.get_db)):
    service = UsuarioService(db)
    usuario = await service.obtener_usuario_por_id(usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

@router.delete("/{usuario_id}")
async def borrar_usuario(usuario_id: int, db: AsyncSession = Depends(database.get_db)):
    service = UsuarioService(db)
    exito = await service.borrar_usuario(usuario_id)

    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"message": "Usuario borrado exitosamente"}

