from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .Usuario_schema import UsuarioCreate, UsuarioLogin, UsuarioRead, UsuarioUpdate
from .Usuario_service import UsuarioService
from src.security import crear_acces_token
from fastapi.security import OAuth2PasswordRequestForm
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
async def inicio_sesion(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(database.get_db)
    ):
    service = UsuarioService(db)
    usuario = await service.login_usuario(form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token_data = {"sub": str(usuario.id), "rol": usuario.rol}
    token = crear_acces_token(data=token_data)
    return  {"access_token" : token, "token_type": "bearer"}


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

@router.put("/{usuario_id}", response_model=UsuarioRead)
async def actualizar_usuario(
    usuario_id: int, 
    datos: UsuarioUpdate, 
    db: AsyncSession = Depends(database.get_db),
    # Descomenta la siguiente línea si quieres obligar a que usen JWT para actualizar:
    # usuario_actual: int = Depends(obtener_usuario_actual) 
):
    service = UsuarioService(db)
    usuario_actualizado = await service.actualizar_usuario(datos, usuario_id)
    
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return usuario_actualizado