import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.security import secret_key, algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

async def obtener_usuario_actual(token:str = Depends(oauth2_scheme)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise credenciales_exception
    except jwt.PyJWTError:
        raise credenciales_exception
    
    return int(usuario_id)