from datetime import datetime, timedelta, timezone
import jwt

secret_key = "Ilar-617"
algorithm = "HS256"
access_token_expire_minutes = 60

def crear_acces_token(data:dict):
    a_encriptar = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)
    a_encriptar.update({"exp": expiracion})

    token_codificado = jwt.encode(a_encriptar, secret_key, algorithm = algorithm)
    return token_codificado