from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import update
from passlib.context import CryptContext
from .Usuario_modelo import Usuario
from .Usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioRead, UsuarioLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:
    def __init__(self,db: AsyncSession):
        self.db = db
    
    def generar_hash(self, password:str) -> str:
        return pwd_context.hash(password)
    
    async def crear_usuario(self, datos:UsuarioCreate):
        password_hash = self.generar_hash(datos.password)

        nuevo_usuario = Usuario(
            correo = datos.correo,
            password = password_hash,
            rol = datos.rol,
            nombre = datos.nombre
        )
        
        self.db.add(nuevo_usuario)
        await self.db.commit()
        await self.db.refresh(nuevo_usuario)
        return nuevo_usuario
    
    async def obtener_usuario_por_id(self, usuario_id: int):
        query = select(Usuario).where(usuario_id == Usuario.id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def listar_todos(self):
        query = select(Usuario)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def login_usuario(self, username:str, password:str):
        query = select(Usuario).where(username == Usuario.correo)
        result = await self.db.execute(query)
        usuario = result.scalar_one_or_none()
        if usuario and pwd_context.verify(password, usuario.password):
            return usuario
        return None

    async def borrar_usuario(self, usuario_id:int):
        usuario = await self.obtener_usuario_por_id(usuario_id)
        if usuario:
            await self.db.delete(usuario)
            await self.db.commit()
            return True
        return False

    async def actualizar_usuario(self, data:UsuarioUpdate,usuario_id:int):
        usuario = await self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return None
        if data.correo is not None:
            await self.db.execute(update(Usuario).where(Usuario.id == usuario_id).values(correo = data.correo))
        if data.password is not None:
            password_hash = self.generar_hash(data.password)
            await self.db.execute(update(Usuario).where(Usuario.id == usuario_id).values(password = password_hash))
        if data.rol is not None:
            await self.db.execute(update(Usuario).where(Usuario.id == usuario_id).values(rol = data.rol))
        if data.nombre is not None:
            await self.db.execute(update(Usuario).where(Usuario.id == usuario_id).values(nombre = data.nombre))
        await self.db.commit()
        return await self.obtener_usuario_por_id(usuario_id)
    
        
    