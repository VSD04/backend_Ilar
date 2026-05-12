from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from .Usuario_modelo import Usuario
from .Usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioRead

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