from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base: presente en todos
class UsuarioBase(BaseModel):
    correo: EmailStr = Field(...,example="usuario@example.com")
    rol: int = Field()
    nombre: Optional[str] = Field(None, max_length=255)

#Create: solo para registro, contiene contraseña
class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, example="Contraseña123!")

#Update: para edicion, todo opcional
class UsuarioUpdate(BaseModel):
    correo: Optional[EmailStr] = Field(None,example="usuario@example.com")
    password: Optional[str] = Field(None, min_length=8)
    rol: Optional[int] = None
    nombre: Optional[str] = Field(None, max_length=255)

#Read: Respuesta para el frontend, no incluye contraseña
class UsuarioRead(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)